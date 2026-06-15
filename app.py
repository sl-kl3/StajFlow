import os
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    Flask, render_template, redirect, url_for, request, flash, abort, send_from_directory,
)
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import (
    db, User, Company, InternshipProgram, Internship, DailyLog, University, StudentDocument,
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from db_seed import init_database, normalize_role, is_danisman, default_university_name

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
upload_path = os.path.join(instance_path, 'uploads')

app = Flask(__name__, instance_path=instance_path)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'stajflow_full_power_123')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///' + os.path.join(instance_path, 'stajflow.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = upload_path
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.context_processor
def inject_globals():
    uni = University.query.first()
    return {
        'institution_name': uni.name if uni else default_university_name(),
        'user_role': normalize_role(current_user.role) if current_user.is_authenticated else None,
        'today_str': datetime.now().strftime('%d.%m.%Y'),
    }


@app.template_filter('status_badge')
def status_badge(status):
    if not status:
        return 'beklemede'
    key = status.strip().lower().replace(' ', '-')
    if key == 'onaylandi':
        return 'onaylandı'
    return key


def role_required(*roles):
    normalized = {normalize_role(r) for r in roles}

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if normalize_role(current_user.role) not in normalized:
                flash('Bu işlem için yetkiniz yok.', 'error')
                return redirect(role_home())
            return view(*args, **kwargs)
        return wrapped
    return decorator


def role_home():
    role = normalize_role(current_user.role)
    if role == 'admin':
        return url_for('admin_home')
    if role == 'danisman':
        return url_for('danisman_home')
    return url_for('ogrenci_home')


def active_internship(student_id):
    return (
        Internship.query.filter_by(student_id=student_id)
        .filter(Internship.status.in_(['Onay Bekliyor', 'Onaylandı']))
        .order_by(Internship.id.desc())
        .first()
    )


def program_slots_left(program):
    taken = Internship.query.filter_by(program_id=program.id).filter(
        Internship.status.in_(['Onay Bekliyor', 'Onaylandı'])
    ).count()
    return max(0, program.quota - taken)


def student_programs():
    programs = (
        InternshipProgram.query.filter_by(is_active=True)
        .join(Company)
        .filter(Company.is_active == True)
        .order_by(InternshipProgram.id.desc())
        .all()
    )
    for p in programs:
        p.slots_left = program_slots_left(p)
    return programs


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_document(student_id, file, doc_type):
    if not file or not file.filename:
        return True
    if not allowed_file(file.filename):
        flash('Geçersiz dosya türü. PDF, Word veya görsel yükleyin.', 'error')
        return False
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    safe = secure_filename(file.filename)
    stored = f'{student_id}_{doc_type}_{int(datetime.utcnow().timestamp())}_{safe}'
    existing = StudentDocument.query.filter_by(student_id=student_id, doc_type=doc_type).first()
    if existing:
        old_path = os.path.join(app.config['UPLOAD_FOLDER'], existing.filename)
        if os.path.isfile(old_path):
            os.remove(old_path)
        existing.filename = stored
        existing.original_name = file.filename
        existing.uploaded_at = datetime.utcnow()
    else:
        db.session.add(StudentDocument(
            student_id=student_id,
            doc_type=doc_type,
            filename=stored,
            original_name=file.filename,
        ))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], stored))
    return True


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '') or request.form.get('sifre', '')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            user.role = normalize_role(user.role)
            db.session.commit()
            login_user(user)
            flash(f'Hoş geldin, {user.name}!', 'success')
            return redirect(url_for('dashboard'))

        flash('E-posta veya şifre hatalı.', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Güvenli çıkış yapıldı.', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(role_home())


@app.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    filename = os.path.basename(filename)
    role = normalize_role(current_user.role)
    if role not in ('admin', 'danisman') and not filename.startswith(f'{current_user.id}_'):
        abort(403)
    folder = app.config['UPLOAD_FOLDER']
    if not os.path.isfile(os.path.join(folder, filename)):
        abort(404)
    return send_from_directory(folder, filename)


# ── Öğrenci sayfaları ──────────────────────────────────────────────

@app.route('/ogrenci')
@login_required
@role_required('ogrenci')
def ogrenci_home():
    apply = active_internship(current_user.id)
    approved = Internship.query.filter_by(student_id=current_user.id, status='Onaylandı').first()
    all_applies = Internship.query.filter_by(student_id=current_user.id).all()
    logs = DailyLog.query.filter_by(student_id=current_user.id).all()
    week_start = datetime.utcnow() - timedelta(days=7)
    logs_week = [l for l in logs if l.date >= week_start]

    return render_template(
        'ogrenci/anasayfa.html',
        active_page='anasayfa',
        page_title='Ana Sayfa',
        apply=apply,
        approved=approved,
        documents=StudentDocument.query.filter_by(student_id=current_user.id).all(),
        stats={
            'bekleyen': sum(1 for a in all_applies if a.status == 'Onay Bekliyor'),
            'toplam_basvuru': len(all_applies),
            'gunluk_toplam': len(logs),
            'gunluk_hafta': len(logs_week),
        },
    )


@app.route('/ogrenci/profil', methods=['POST'])
@login_required
@role_required('ogrenci')
def ogrenci_profil():
    gpa = request.form.get('gpa', type=float)
    if gpa is not None and not (0 <= gpa <= 4):
        flash('GANO 0 ile 4 arasında olmalı.', 'error')
        return redirect(url_for('ogrenci_home'))
    current_user.gpa = gpa
    current_user.graduated_school = request.form.get('graduated_school', '').strip() or None
    current_user.department = request.form.get('department', '').strip() or None
    current_user.experience = request.form.get('experience', '').strip() or None
    current_user.foreign_language = request.form.get('foreign_language', '').strip() or None
    current_user.phone = request.form.get('phone', '').strip() or None

    upload_ok = True
    for doc_type in ('cv', 'diploma', 'certificate', 'other'):
        f = request.files.get(doc_type)
        if f and f.filename and not allowed_file(f.filename):
            flash('Geçersiz dosya türü. PDF, Word veya görsel yükleyin.', 'error')
            return redirect(url_for('ogrenci_home'))

    for doc_type in ('cv', 'diploma', 'certificate', 'other'):
        if not save_document(current_user.id, request.files.get(doc_type), doc_type):
            upload_ok = False

    if upload_ok:
        db.session.commit()
        flash('Profil ve belgeler güncellendi.', 'success')
    else:
        db.session.rollback()
    return redirect(url_for('ogrenci_home'))


@app.route('/ogrenci/ilanlar')
@login_required
@role_required('ogrenci')
def ogrenci_ilanlar():
    apply = active_internship(current_user.id)
    can_apply = apply is None or apply.status == 'Reddedildi'
    return render_template(
        'ogrenci/ilanlar.html',
        active_page='ilanlar',
        page_title='Staj İlanları',
        programs=student_programs(),
        can_apply=can_apply,
        apply=apply,
    )


@app.route('/ogrenci/basvurularim')
@login_required
@role_required('ogrenci')
def ogrenci_basvurularim():
    applies = (
        Internship.query.filter_by(student_id=current_user.id)
        .order_by(Internship.id.desc())
        .all()
    )
    return render_template(
        'ogrenci/basvurularim.html',
        active_page='basvurularim',
        page_title='Başvurularım',
        applies=applies,
    )


@app.route('/ogrenci/gunluk')
@login_required
@role_required('ogrenci')
def ogrenci_gunluk():
    apply = Internship.query.filter_by(student_id=current_user.id, status='Onaylandı').first()
    logs = DailyLog.query.filter_by(student_id=current_user.id).order_by(DailyLog.date.desc()).all()
    return render_template(
        'ogrenci/gunluk.html',
        active_page='gunluk',
        page_title='Staj Günlüğüm',
        apply=apply,
        logs=logs,
    )


@app.route('/ogrenci/degerlendirme')
@login_required
@role_required('ogrenci')
def ogrenci_degerlendirme():
    apply = (
        Internship.query.filter_by(student_id=current_user.id)
        .filter(Internship.score.isnot(None))
        .order_by(Internship.id.desc())
        .first()
    )
    logs = DailyLog.query.filter_by(student_id=current_user.id).order_by(DailyLog.date.desc()).all()
    return render_template(
        'ogrenci/degerlendirme.html',
        active_page='degerlendirme',
        page_title='Değerlendirme',
        apply=apply,
        logs=logs,
    )


@app.route('/apply_program/<int:program_id>', methods=['POST'])
@login_required
@role_required('ogrenci')
def apply_program(program_id):
    if active_internship(current_user.id):
        flash('Zaten aktif veya bekleyen bir staj başvurunuz var.', 'error')
        return redirect(url_for('ogrenci_ilanlar'))

    program = InternshipProgram.query.filter_by(id=program_id, is_active=True).first_or_404()
    if not program.company.is_active:
        flash('Bu şirketin ilanı artık aktif değil.', 'error')
        return redirect(url_for('ogrenci_ilanlar'))

    if program_slots_left(program) <= 0:
        flash('Bu staj programı için kontenjan dolmuş.', 'error')
        return redirect(url_for('ogrenci_ilanlar'))

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
    flash(f'"{program.title}" programına başvurunuz gönderildi.', 'success')
    return redirect(url_for('ogrenci_basvurularim'))


@app.route('/add_log', methods=['POST'])
@login_required
@role_required('ogrenci')
def add_log():
    content = request.form.get('content', '').strip()
    if not content:
        flash('Günlük içeriği boş olamaz.', 'error')
        return redirect(url_for('ogrenci_gunluk'))

    if not Internship.query.filter_by(student_id=current_user.id, status='Onaylandı').first():
        flash('Günlük eklemek için onaylanmış bir stajınız olmalı.', 'error')
        return redirect(url_for('ogrenci_gunluk'))

    hours = request.form.get('hours', type=int)
    if not hours or not (1 <= hours <= 12):
        flash('Çalışılan saat 1–12 arasında olmalı.', 'error')
        return redirect(url_for('ogrenci_gunluk'))

    db.session.add(DailyLog(
        student_id=current_user.id,
        student_name=current_user.name,
        content=content,
        hours=hours,
        status='Beklemede',
    ))
    db.session.commit()
    flash('Günlük kaydınız danışmana gönderildi.', 'success')
    return redirect(url_for('ogrenci_gunluk'))


# ── Danışman sayfaları ─────────────────────────────────────────────

@app.route('/danisman')
@login_required
@role_required('danisman')
def danisman_home():
    applies = Internship.query.filter_by(status='Onay Bekliyor').count()
    logs = DailyLog.query.filter_by(status='Beklemede').count()
    return render_template(
        'danisman/anasayfa.html',
        active_page='anasayfa',
        page_title='Ana Sayfa',
        stats={
            'bekleyen_basvuru': applies,
            'bekleyen_gunluk': logs,
            'onaylanan': Internship.query.filter_by(status='Onaylandı').count(),
            'reddedilen': Internship.query.filter_by(status='Reddedildi').count(),
        },
    )


@app.route('/danisman/basvurular')
@login_required
@role_required('danisman')
def danisman_basvurular():
    applies = (
        Internship.query.filter_by(status='Onay Bekliyor')
        .order_by(Internship.id.desc())
        .all()
    )
    return render_template(
        'danisman/basvuru-onay.html',
        active_page='basvurular',
        page_title='Başvuru Onayı',
        applies=applies,
    )


@app.route('/danisman/gunluk')
@login_required
@role_required('danisman')
def danisman_gunluk():
    logs = DailyLog.query.filter_by(status='Beklemede').order_by(DailyLog.date.desc()).all()
    return render_template(
        'danisman/gunluk-onay.html',
        active_page='gunluk',
        page_title='Günlük Onayı',
        logs=logs,
    )


@app.route('/danisman/puanlama')
@login_required
@role_required('danisman')
def danisman_puanlama():
    onaylananlar = (
        Internship.query.filter_by(status='Onaylandı')
        .order_by(Internship.id.desc())
        .all()
    )
    return render_template(
        'danisman/puanlama.html',
        active_page='puanlama',
        page_title='Staj Puanlama',
        onaylananlar=onaylananlar,
    )


@app.route('/action/apply/<int:apply_id>/<action>', methods=['POST'])
@login_required
@role_required('danisman')
def action_apply(apply_id, action):
    record = Internship.query.get_or_404(apply_id)
    if action == 'ok':
        record.status = 'Onaylandı'
        flash('Staj başvurusu onaylandı.', 'success')
    elif action == 'no':
        record.status = 'Reddedildi'
        flash('Staj başvurusu reddedildi.', 'success')
    else:
        abort(400)
    db.session.commit()
    return redirect(url_for('danisman_basvurular'))


@app.route('/action/log/<int:log_id>/<action>', methods=['POST'])
@login_required
@role_required('danisman')
def action_log(log_id, action):
    record = DailyLog.query.get_or_404(log_id)
    if action == 'ok':
        record.status = 'Onaylandı'
        flash('Günlük kaydı onaylandı.', 'success')
    elif action == 'no':
        record.status = 'Reddedildi'
        flash('Günlük kaydı reddedildi.', 'success')
    else:
        abort(400)
    db.session.commit()
    return redirect(url_for('danisman_gunluk'))


@app.route('/action/score/<int:apply_id>', methods=['POST'])
@login_required
@role_required('danisman')
def action_score(apply_id):
    record = Internship.query.get_or_404(apply_id)
    if record.status != 'Onaylandı':
        flash('Sadece onaylanmış stajlar puanlanabilir.', 'error')
        return redirect(url_for('danisman_puanlama'))
    score = request.form.get('score', type=int)
    note = request.form.get('advisor_note', '').strip()
    if score is None or not (0 <= score <= 100):
        flash('Geçerli bir puan girin (0-100).', 'error')
        return redirect(url_for('danisman_puanlama'))
    record.score = score
    record.advisor_note = note or None
    db.session.commit()
    flash(f'{record.student.name} için puan kaydedildi: {score}/100', 'success')
    return redirect(url_for('danisman_puanlama'))


# ── Admin sayfaları ─────────────────────────────────────────────────

def admin_stats():
    users = User.query.all()
    return {
        'total': len(users),
        'ogrenci': sum(1 for u in users if normalize_role(u.role) == 'ogrenci'),
        'danisman': sum(1 for u in users if is_danisman(u.role)),
        'bekleyen_basvuru': Internship.query.filter_by(status='Onay Bekliyor').count(),
        'onaylanan': Internship.query.filter_by(status='Onaylandı').count(),
        'reddedilen': Internship.query.filter_by(status='Reddedildi').count(),
        'program_sayisi': InternshipProgram.query.filter_by(is_active=True).count(),
        'sirket_sayisi': Company.query.filter_by(is_active=True).count(),
    }


@app.route('/admin')
@login_required
@role_required('admin')
def admin_home():
    internships = Internship.query.order_by(Internship.id.desc()).limit(20).all()
    return render_template(
        'admin/anasayfa.html',
        active_page='anasayfa',
        page_title='Dashboard',
        stats=admin_stats(),
        internships=internships,
    )


@app.route('/admin/ogrenciler')
@login_required
@role_required('admin')
def admin_ogrenciler():
    users = User.query.order_by(User.role, User.name).all()
    return render_template(
        'admin/ogrenciler.html',
        active_page='ogrenciler',
        page_title='Öğrenciler',
        users=users,
    )


@app.route('/admin/basvurular')
@login_required
@role_required('admin')
def admin_basvurular():
    internships = Internship.query.order_by(Internship.id.desc()).all()
    return render_template(
        'admin/basvurular.html',
        active_page='basvurular',
        page_title='Başvurular',
        internships=internships,
    )


@app.route('/admin/sirketler')
@login_required
@role_required('admin')
def admin_sirketler():
    companies = Company.query.order_by(Company.name).all()
    programs = (
        InternshipProgram.query.order_by(InternshipProgram.is_active.desc(), InternshipProgram.id.desc()).all()
    )
    return render_template(
        'admin/sirketler.html',
        active_page='sirketler',
        page_title='Şirketler',
        companies=companies,
        programs=programs,
    )


@app.route('/admin/raporlar')
@login_required
@role_required('admin')
def admin_raporlar():
    return render_template(
        'admin/raporlar.html',
        active_page='raporlar',
        page_title='Raporlar',
        stats=admin_stats(),
    )


@app.route('/admin/add_user', methods=['POST'])
@login_required
@role_required('admin')
def admin_add_user():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    role = normalize_role(request.form.get('role', 'ogrenci'))

    if not all([name, email, password]):
        flash('Tüm alanları doldurun.', 'error')
        return redirect(url_for('admin_ogrenciler'))

    if User.query.filter_by(email=email).first():
        flash('Bu e-posta zaten kayıtlı.', 'error')
        return redirect(url_for('admin_ogrenciler'))

    uni = University.query.filter_by(is_active=True).first()
    db.session.add(User(
        email=email,
        password=generate_password_hash(password),
        name=name,
        role=role,
        student_no=request.form.get('student_no', '').strip() or None,
        department=request.form.get('department', '').strip() or None,
        university_id=uni.id if uni else None,
    ))
    db.session.commit()
    flash(f'{name} eklendi.', 'success')
    return redirect(url_for('admin_ogrenciler'))


@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Kendi hesabınızı silemezsiniz.', 'error')
        return redirect(url_for('admin_ogrenciler'))
    docs = StudentDocument.query.filter_by(student_id=user.id).all()
    for doc in docs:
        path = os.path.join(app.config['UPLOAD_FOLDER'], doc.filename)
        if os.path.isfile(path):
            os.remove(path)
    StudentDocument.query.filter_by(student_id=user.id).delete()
    DailyLog.query.filter_by(student_id=user.id).delete()
    Internship.query.filter_by(student_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('Kullanıcı silindi.', 'success')
    return redirect(url_for('admin_ogrenciler'))


@app.route('/admin/add_company', methods=['POST'])
@login_required
@role_required('admin')
def admin_add_company():
    name = request.form.get('name', '').strip()
    if not name:
        flash('Şirket adı zorunlu.', 'error')
        return redirect(url_for('admin_sirketler'))
    db.session.add(Company(
        name=name,
        sector=request.form.get('sector', '').strip() or None,
        contact=request.form.get('contact', '').strip() or None,
        address=request.form.get('address', '').strip() or None,
    ))
    db.session.commit()
    flash(f'Şirket "{name}" eklendi.', 'success')
    return redirect(url_for('admin_sirketler'))


@app.route('/admin/add_program', methods=['POST'])
@login_required
@role_required('admin')
def admin_add_program():
    company_id = request.form.get('company_id', type=int)
    title = request.form.get('title', '').strip()
    if not company_id or not title:
        flash('Şirket ve program başlığı zorunlu.', 'error')
        return redirect(url_for('admin_sirketler'))

    db.session.add(InternshipProgram(
        company_id=company_id,
        title=title,
        description=request.form.get('description', '').strip() or None,
        internship_type=request.form.get('type', 'Zorunlu'),
        start_date=request.form.get('start', ''),
        end_date=request.form.get('end', '') or None,
        quota=request.form.get('quota', 5, type=int) or 5,
        is_active=True,
    ))
    db.session.commit()
    flash(f'Staj programı "{title}" yayınlandı.', 'success')
    return redirect(url_for('admin_sirketler'))


@app.route('/admin/toggle_program/<int:program_id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_toggle_program(program_id):
    program = InternshipProgram.query.get_or_404(program_id)
    program.is_active = not program.is_active
    db.session.commit()
    durum = 'açıldı' if program.is_active else 'kapatıldı'
    flash(f'Program {durum}.', 'success')
    return redirect(url_for('admin_sirketler'))


with app.app_context():
    init_database(app)
    os.makedirs(upload_path, exist_ok=True)


if __name__ == '__main__':
    app.run(debug=True)
