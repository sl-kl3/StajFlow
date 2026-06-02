import os
from functools import wraps

from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Company, InternshipProgram, Internship, DailyLog
from db_seed import init_database, normalize_role

# --- panel menuleri (her rol icin) ---
MENULER = {
    'ogrenci': [
        ('ozet', 'Ana Sayfa', 'ti-home'),
        ('ilanlar', 'Staj İlanları', 'ti-building'),
        ('basvurularim', 'Başvurularım', 'ti-file-text'),
        ('gunluk', 'Staj Günlüğüm', 'ti-notebook'),
        ('degerlendirme', 'Değerlendirmem', 'ti-star'),
    ],
    'danisman': [
        ('ozet', 'Ana Sayfa', 'ti-home'),
        ('basvuru-onay', 'Başvuru Onayı', 'ti-briefcase'),
        ('gunluk-onay', 'Günlük Onayı', 'ti-notebook'),
        ('gecmis', 'Son İşlemler', 'ti-history'),
    ],
    'admin': [
        ('ozet', 'Ana Sayfa', 'ti-home'),
        ('ogrenciler', 'Kullanıcılar', 'ti-users'),
        ('basvurular', 'Başvurular', 'ti-file-check'),
        ('sirketler', 'Şirketler', 'ti-building'),
    ],
}

BASLIKLAR = {
    'ogrenci': {
        'ozet': ('Ana Sayfa', 'Staj takibine genel bakış'),
        'ilanlar': ('Staj İlanları', 'Açık ilanlara başvur'),
        'basvurularim': ('Başvurularım', 'Başvuru durumun'),
        'gunluk': ('Staj Günlüğüm', 'Günlük yaz ve listele'),
        'degerlendirme': ('Değerlendirmem', 'Onay durumları'),
    },
    'danisman': {
        'ozet': ('Ana Sayfa', 'Bekleyen işlemler'),
        'basvuru-onay': ('Başvuru Onayı', 'Staj başvuruları'),
        'gunluk-onay': ('Günlük Onayı', 'Öğrenci günlükleri'),
        'gecmis': ('Son İşlemler', 'Geçmiş kayıtlar'),
    },
    'admin': {
        'ozet': ('Ana Sayfa', 'Sistem özeti'),
        'ogrenciler': ('Kullanıcılar', 'Kayıtlı kullanıcılar'),
        'basvurular': ('Başvurular', 'Tüm staj başvuruları'),
        'sirketler': ('Şirketler', 'Şirket ve ilan yönetimi'),
    },
}

ROL_ETIKET = {'admin': 'Admin', 'danisman': 'Danışman', 'ogrenci': 'Öğrenci'}

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')

app = Flask(__name__, instance_path=instance_path)
app.config['SECRET_KEY'] = 'stajflow_gizli_anahtar_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'stajflow.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.context_processor
def sablon_yardimcilari():
    rol = normalize_role(current_user.role) if current_user.is_authenticated else None
    return {
        'normalize_role': normalize_role,
        'user_role': rol,
        'panel_menus': MENULER.get(rol, []),
        'role_label': ROL_ETIKET.get(rol, ''),
    }


def rol_gerekli(*roller):
    izinli = {normalize_role(r) for r in roller}

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if normalize_role(current_user.role) not in izinli:
                flash('Bu sayfaya erişim yetkiniz yok.', 'error')
                return redirect(url_for('panel'))
            return view(*args, **kwargs)
        return wrapped
    return decorator


def aktif_basvuru(ogrenci_id):
    """Onay bekleyen veya onaylanmis basvuru - yeni basvuruyu engeller."""
    return Internship.query.filter_by(student_id=ogrenci_id).filter(
        Internship.status.in_(['Onay Bekliyor', 'Onaylandı'])
    ).order_by(Internship.id.desc()).first()


def son_basvuru(ogrenci_id):
    """Ekranda gosterilecek son basvuru (red dahil)."""
    return Internship.query.filter_by(student_id=ogrenci_id).order_by(
        Internship.id.desc()
    ).first()


def kontenjan_kalan(program):
    dolu = Internship.query.filter_by(program_id=program.id).filter(
        Internship.status.in_(['Onay Bekliyor', 'Onaylandı'])
    ).count()
    return max(0, program.quota - dolu)


@login_manager.user_loader
def kullanici_yukle(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('panel'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('panel'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        sifre = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, sifre):
            login_user(user)
            flash('Hoş geldin, ' + user.name + '!', 'success')
            return redirect(url_for('panel'))
        flash('E-posta veya şifre hatalı.', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def admin_verileri():
    users = User.query.order_by(User.name).all()
    return {
        'users': users,
        'stats': {
            'ogrenci': sum(1 for u in users if normalize_role(u.role) == 'ogrenci'),
            'danisman': sum(1 for u in users if normalize_role(u.role) == 'danisman'),
            'bekleyen_basvuru': Internship.query.filter_by(status='Onay Bekliyor').count(),
            'bekleyen_gunluk': DailyLog.query.filter_by(status='Beklemede').count(),
            'program_sayisi': InternshipProgram.query.filter_by(is_active=True).count(),
            'sirket_sayisi': Company.query.count(),
        },
        'companies': Company.query.order_by(Company.name).all(),
        'programs': InternshipProgram.query.order_by(InternshipProgram.id.desc()).all(),
        'internships': Internship.query.order_by(Internship.id.desc()).all(),
    }


def danisman_verileri():
    bekleyen_basvuru = Internship.query.filter_by(status='Onay Bekliyor').order_by(
        Internship.id.desc()
    ).all()
    bekleyen_gunluk = DailyLog.query.filter_by(status='Beklemede').order_by(
        DailyLog.date.desc()
    ).all()
    return {
        'applies': bekleyen_basvuru,
        'logs': bekleyen_gunluk,
        'recent_applies': Internship.query.filter(
            Internship.status != 'Onay Bekliyor'
        ).order_by(Internship.id.desc()).limit(8).all(),
        'approved_logs': DailyLog.query.filter(
            DailyLog.status != 'Beklemede'
        ).order_by(DailyLog.date.desc()).limit(10).all(),
        'stats': {
            'bekleyen_basvuru': len(bekleyen_basvuru),
            'bekleyen_gunluk': len(bekleyen_gunluk),
            'toplam_bekleyen': len(bekleyen_basvuru) + len(bekleyen_gunluk),
            'onaylanan': Internship.query.filter_by(status='Onaylandı').count(),
            'reddedilen': Internship.query.filter_by(status='Reddedildi').count(),
        },
    }


def ogrenci_verileri():
    basvuru = son_basvuru(current_user.id)
    engel = aktif_basvuru(current_user.id)
    programs = InternshipProgram.query.filter_by(is_active=True).join(Company).order_by(
        InternshipProgram.id.desc()
    ).all()
    for p in programs:
        p.slots_left = kontenjan_kalan(p)
    return {
        'apply': basvuru,
        'can_apply': engel is None,
        'logs': DailyLog.query.filter_by(student_id=current_user.id).order_by(
            DailyLog.date.desc()
        ).all(),
        'programs': programs,
    }


@app.route('/panel')
@app.route('/panel/<section>')
@login_required
def panel(section=None):
    rol = normalize_role(current_user.role)
    if section is None:
        section = 'ozet'

    izinli = [m[0] for m in MENULER.get(rol, [])]
    if section not in izinli:
        abort(404)

    baslik, alt = BASLIKLAR.get(rol, {}).get(section, ('Panel', ''))
    ctx = {
        'section': section,
        'panel_role': rol,
        'page_title': baslik,
        'page_subtitle': alt,
    }

    if rol == 'admin':
        ctx.update(admin_verileri())
    elif rol == 'danisman':
        ctx.update(danisman_verileri())
    else:
        ctx.update(ogrenci_verileri())

    return render_template('panel.html', **ctx)


@app.route('/apply_program/<int:program_id>', methods=['POST'])
@login_required
@rol_gerekli('ogrenci')
def apply_program(program_id):
    if aktif_basvuru(current_user.id):
        flash('Zaten aktif bir başvurun var.', 'error')
        return redirect(url_for('panel', section='ilanlar'))

    program = InternshipProgram.query.filter_by(id=program_id, is_active=True).first_or_404()
    if kontenjan_kalan(program) <= 0:
        flash('Kontenjan dolmuş.', 'error')
        return redirect(url_for('panel', section='ilanlar'))

    db.session.add(Internship(
        student_id=current_user.id,
        program_id=program.id,
        company_name=program.company.name,
        internship_type=program.internship_type,
        start_date=program.start_date,
        end_date=program.end_date,
        description=program.description,
        status='Onay Bekliyor',
    ))
    db.session.commit()
    flash('Başvurun danışmana gönderildi.', 'success')
    return redirect(url_for('panel', section='basvurularim'))


@app.route('/add_log', methods=['POST'])
@login_required
@rol_gerekli('ogrenci')
def add_log():
    icerik = request.form.get('content', '').strip()
    if not icerik:
        flash('Günlük boş olamaz.', 'error')
        return redirect(url_for('panel', section='gunluk'))

    onayli = Internship.query.filter_by(student_id=current_user.id, status='Onaylandı').first()
    if not onayli:
        flash('Önce staj başvurunun onaylanması lazım.', 'error')
        return redirect(url_for('panel', section='gunluk'))

    db.session.add(DailyLog(
        student_id=current_user.id,
        student_name=current_user.name,
        content=icerik,
        status='Beklemede',
    ))
    db.session.commit()
    flash('Günlük gönderildi.', 'success')
    return redirect(url_for('panel', section='gunluk'))


@app.route('/action/apply/<int:apply_id>/<action>', methods=['POST'])
@login_required
@rol_gerekli('danisman')
def action_apply(apply_id, action):
    kayit = Internship.query.get_or_404(apply_id)
    if action == 'ok':
        kayit.status = 'Onaylandı'
        flash('Başvuru onaylandı.', 'success')
    elif action == 'no':
        kayit.status = 'Reddedildi'
        flash('Başvuru reddedildi.', 'success')
    else:
        abort(400)
    db.session.commit()
    return redirect(url_for('panel', section='basvuru-onay'))


@app.route('/action/log/<int:log_id>/<action>', methods=['POST'])
@login_required
@rol_gerekli('danisman')
def action_log(log_id, action):
    kayit = DailyLog.query.get_or_404(log_id)
    if action == 'ok':
        kayit.status = 'Onaylandı'
        flash('Günlük onaylandı.', 'success')
    elif action == 'no':
        kayit.status = 'Reddedildi'
        flash('Günlük reddedildi.', 'success')
    else:
        abort(400)
    db.session.commit()
    return redirect(url_for('panel', section='gunluk-onay'))


@app.route('/admin/add_user', methods=['POST'])
@login_required
@rol_gerekli('admin')
def admin_add_user():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    role = normalize_role(request.form.get('role', 'ogrenci'))

    if not all([name, email, password]):
        flash('Tüm alanları doldur.', 'error')
        return redirect(url_for('panel', section='ogrenciler'))

    if User.query.filter_by(email=email).first():
        flash('Bu e-posta zaten var.', 'error')
        return redirect(url_for('panel', section='ogrenciler'))

    db.session.add(User(
        email=email,
        password=generate_password_hash(password),
        name=name,
        role=role,
    ))
    db.session.commit()
    flash(name + ' eklendi.', 'success')
    return redirect(url_for('panel', section='ogrenciler'))


@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
@rol_gerekli('admin')
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Kendi hesabını silemezsin.', 'error')
        return redirect(url_for('panel', section='ogrenciler'))
    DailyLog.query.filter_by(student_id=user.id).delete()
    Internship.query.filter_by(student_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('Kullanıcı silindi.', 'success')
    return redirect(url_for('panel', section='ogrenciler'))


@app.route('/admin/add_company', methods=['POST'])
@login_required
@rol_gerekli('admin')
def admin_add_company():
    name = request.form.get('name', '').strip()
    if not name:
        flash('Şirket adı gerekli.', 'error')
        return redirect(url_for('panel', section='sirketler'))
    db.session.add(Company(
        name=name,
        sector=request.form.get('sector', '').strip() or None,
        contact=request.form.get('contact', '').strip() or None,
        address=request.form.get('address', '').strip() or None,
    ))
    db.session.commit()
    flash('Şirket eklendi.', 'success')
    return redirect(url_for('panel', section='sirketler'))


@app.route('/admin/add_program', methods=['POST'])
@login_required
@rol_gerekli('admin')
def admin_add_program():
    company_id = request.form.get('company_id', type=int)
    title = request.form.get('title', '').strip()
    if not company_id or not title:
        flash('Şirket ve ilan başlığı gerekli.', 'error')
        return redirect(url_for('panel', section='sirketler'))

    db.session.add(InternshipProgram(
        company_id=company_id,
        title=title,
        description=request.form.get('description', '').strip() or None,
        internship_type=request.form.get('type', 'Zorunlu'),
        start_date=request.form.get('start', ''),
        end_date=request.form.get('end', '') or None,
        quota=request.form.get('quota', 3, type=int) or 3,
        is_active=True,
    ))
    db.session.commit()
    flash('İlan yayınlandı.', 'success')
    return redirect(url_for('panel', section='sirketler'))


@app.route('/admin/toggle_program/<int:program_id>', methods=['POST'])
@login_required
@rol_gerekli('admin')
def admin_toggle_program(program_id):
    program = InternshipProgram.query.get_or_404(program_id)
    program.is_active = not program.is_active
    db.session.commit()
    flash('İlan durumu güncellendi.', 'success')
    return redirect(url_for('panel', section='sirketler'))


with app.app_context():
    init_database(app)


if __name__ == '__main__':
    app.run(debug=True)
