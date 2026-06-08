import os
from functools import wraps

from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Company, InternshipProgram, Internship, DailyLog
from werkzeug.security import generate_password_hash, check_password_hash
from db_seed import init_database, normalize_role, is_danisman

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')

app = Flask(__name__, instance_path=instance_path)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'stajflow_full_power_123')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///' + os.path.join(instance_path, 'stajflow.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


def role_required(*roles):
    normalized = {normalize_role(r) for r in roles}

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if normalize_role(current_user.role) not in normalized:
                flash('Bu işlem için yetkiniz yok.', 'error')
                return redirect(url_for('dashboard'))
            return view(*args, **kwargs)
        return wrapped
    return decorator


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
    role = normalize_role(current_user.role)

    if role == 'admin':
        users = User.query.order_by(User.role, User.name).all()
        companies = Company.query.order_by(Company.name).all()
        programs = (
            InternshipProgram.query.order_by(InternshipProgram.is_active.desc(), InternshipProgram.id.desc()).all()
        )
        stats = {
            'total': len(users),
            'ogrenci': sum(1 for u in users if normalize_role(u.role) == 'ogrenci'),
            'danisman': sum(1 for u in users if is_danisman(u.role)),
            'bekleyen_basvuru': Internship.query.filter_by(status='Onay Bekliyor').count(),
            'bekleyen_gunluk': DailyLog.query.filter_by(status='Beklemede').count(),
            'program_sayisi': InternshipProgram.query.filter_by(is_active=True).count(),
            'sirket_sayisi': Company.query.filter_by(is_active=True).count(),
        }
        return render_template(
            'admin.html', users=users, stats=stats, companies=companies, programs=programs
        )

    if role == 'danisman':
        logs = DailyLog.query.filter_by(status='Beklemede').order_by(DailyLog.date.desc()).all()
        applies = (
            Internship.query.filter_by(status='Onay Bekliyor')
            .order_by(Internship.id.desc())
            .all()
        )
        approved_logs = (
            DailyLog.query.filter(DailyLog.status != 'Beklemede')
            .order_by(DailyLog.date.desc())
            .limit(10)
            .all()
        )
        recent_applies = (
            Internship.query.filter(Internship.status != 'Onay Bekliyor')
            .order_by(Internship.id.desc())
            .limit(8)
            .all()
        )
        return render_template(
            'advisor.html',
            logs=logs,
            applies=applies,
            approved_logs=approved_logs,
            recent_applies=recent_applies,
            stats={
                'bekleyen_basvuru': len(applies),
                'bekleyen_gunluk': len(logs),
                'toplam_bekleyen': len(applies) + len(logs),
                'onaylanan': Internship.query.filter_by(status='Onaylandı').count(),
                'reddedilen': Internship.query.filter_by(status='Reddedildi').count(),
            },
        )

    logs = DailyLog.query.filter_by(student_id=current_user.id).order_by(DailyLog.date.desc()).all()
    apply = active_internship(current_user.id)
    programs = (
        InternshipProgram.query.filter_by(is_active=True)
        .join(Company)
        .filter(Company.is_active == True)
        .order_by(InternshipProgram.id.desc())
        .all()
    )
    for p in programs:
        p.slots_left = program_slots_left(p)
    can_apply = apply is None or apply.status == 'Reddedildi'
    return render_template(
        'student.html', logs=logs, apply=apply, programs=programs, can_apply=can_apply
    )


@app.route('/apply_program/<int:program_id>', methods=['POST'])
@login_required
@role_required('ogrenci')
def apply_program(program_id):
    if active_internship(current_user.id):
        flash('Zaten aktif veya bekleyen bir staj başvurunuz var.', 'error')
        return redirect(url_for('dashboard'))

    program = InternshipProgram.query.filter_by(id=program_id, is_active=True).first_or_404()
    if not program.company.is_active:
        flash('Bu şirketin ilanı artık aktif değil.', 'error')
        return redirect(url_for('dashboard'))

    if program_slots_left(program) <= 0:
        flash('Bu staj programı için kontenjan dolmuş.', 'error')
        return redirect(url_for('dashboard'))

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
    flash(f'"{program.title}" programına başvurunuz danışmana gönderildi.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/add_log', methods=['POST'])
@login_required
@role_required('ogrenci')
def add_log():
    content = request.form.get('content', '').strip()
    if not content:
        flash('Günlük içeriği boş olamaz.', 'error')
        return redirect(url_for('dashboard'))

    if not Internship.query.filter_by(student_id=current_user.id, status='Onaylandı').first():
        flash('Günlük eklemek için onaylanmış bir stajınız olmalı.', 'error')
        return redirect(url_for('dashboard'))

    db.session.add(DailyLog(
        student_id=current_user.id,
        student_name=current_user.name,
        content=content,
        status='Beklemede',
    ))
    db.session.commit()
    flash('Günlük kaydınız danışmana gönderildi.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/action/apply/<int:apply_id>/<action>', methods=['POST'])
@login_required
@role_required('danisman')
def action_apply(apply_id, action):
    record = Internship.query.get_or_404(apply_id)
    if action == 'ok':
        record.status = 'Onaylandı'
        flash('Staj başvurusu onaylandı. Öğrenci günlük girebilir.', 'success')
    elif action == 'no':
        record.status = 'Reddedildi'
        flash('Staj başvurusu reddedildi.', 'success')
    else:
        abort(400)
    db.session.commit()
    return redirect(url_for('dashboard'))


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
    return redirect(url_for('dashboard'))


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
        return redirect(url_for('dashboard'))

    if User.query.filter_by(email=email).first():
        flash('Bu e-posta zaten kayıtlı.', 'error')
        return redirect(url_for('dashboard'))

    db.session.add(User(
        email=email,
        password=generate_password_hash(password),
        name=name,
        role=role,
    ))
    db.session.commit()
    flash(f'{name} eklendi.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Kendi hesabınızı silemezsiniz.', 'error')
        return redirect(url_for('dashboard'))
    DailyLog.query.filter_by(student_id=user.id).delete()
    Internship.query.filter_by(student_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('Kullanıcı silindi.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/admin/add_company', methods=['POST'])
@login_required
@role_required('admin')
def admin_add_company():
    name = request.form.get('name', '').strip()
    if not name:
        flash('Şirket adı zorunlu.', 'error')
        return redirect(url_for('dashboard'))
    db.session.add(Company(
        name=name,
        sector=request.form.get('sector', '').strip() or None,
        contact=request.form.get('contact', '').strip() or None,
        address=request.form.get('address', '').strip() or None,
    ))
    db.session.commit()
    flash(f'Şirket "{name}" eklendi. Şimdi staj programı açabilirsiniz.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/admin/add_program', methods=['POST'])
@login_required
@role_required('admin')
def admin_add_program():
    company_id = request.form.get('company_id', type=int)
    title = request.form.get('title', '').strip()
    if not company_id or not title:
        flash('Şirket ve program başlığı zorunlu.', 'error')
        return redirect(url_for('dashboard'))

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
    flash(f'Staj programı "{title}" yayınlandı. Öğrenciler seçebilir.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/admin/toggle_program/<int:program_id>', methods=['POST'])
@login_required
@role_required('admin')
def admin_toggle_program(program_id):
    program = InternshipProgram.query.get_or_404(program_id)
    program.is_active = not program.is_active
    db.session.commit()
    durum = 'açıldı' if program.is_active else 'kapatıldı'
    flash(f'Program {durum}.', 'success')
    return redirect(url_for('dashboard'))


with app.app_context():
    init_database(app)


if __name__ == '__main__':
    app.run(debug=True)s