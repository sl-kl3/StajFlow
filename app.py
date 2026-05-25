import os
from functools import wraps

from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, DailyLog, Internship
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
            if user.role != normalize_role(user.role):
                user.role = normalize_role(user.role)
                db.session.commit()
            login_user(user)
            flash(f'Hoş geldin, {user.name}!', 'success')
            return redirect(url_for('dashboard'))

        flash('E-posta veya şifre hatalı. Demo: hoca@staj.edu.tr / hoca123 veya ahmet@staj.edu.tr / dan123', 'error')

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
        stats = {
            'total': len(users),
            'ogrenci': sum(1 for u in users if normalize_role(u.role) == 'ogrenci'),
            'danisman': sum(1 for u in users if is_danisman(u.role)),
            'bekleyen_basvuru': Internship.query.filter_by(status='Onay Bekliyor').count(),
            'bekleyen_gunluk': DailyLog.query.filter_by(status='Beklemede').count(),
        }
        return render_template('admin.html', users=users, stats=stats)

    if role == 'danisman':
        bekleyen = Internship.query.filter_by(status='Onay Bekliyor').count()
        onaylanan = Internship.query.filter_by(status='Onaylandı').count()
        reddedilen = Internship.query.filter_by(status='Reddedildi').count()
        ogrenci_sayisi = User.query.filter(User.role.in_(['ogrenci', 'student'])).count()

        logs = DailyLog.query.filter_by(status='Beklemede').order_by(DailyLog.date.desc()).all()
        applies = (
            Internship.query.filter_by(status='Onay Bekliyor')
            .order_by(Internship.id.desc())
            .all()
        )
        students = User.query.filter(
            db.or_(
                User.role == 'ogrenci',
                User.role == 'student',
            )
        ).order_by(User.name).all()
        all_applies = Internship.query.order_by(Internship.id.desc()).limit(20).all()
        approved_logs = (
            DailyLog.query.filter(DailyLog.status != 'Beklemede')
            .order_by(DailyLog.date.desc())
            .limit(10)
            .all()
        )
        return render_template(
            'advisor.html',
            logs=logs,
            applies=applies,
            approved_logs=approved_logs,
            students=students,
            all_applies=all_applies,
            stats={
                'bekleyen': bekleyen,
                'onaylanan': onaylanan,
                'reddedilen': reddedilen,
                'ogrenci': ogrenci_sayisi,
            },
        )

    logs = DailyLog.query.filter_by(student_id=current_user.id).order_by(
        DailyLog.date.desc()
    ).all()
    apply = (
        Internship.query.filter_by(student_id=current_user.id)
        .order_by(Internship.id.desc())
        .first()
    )
    return render_template('student.html', logs=logs, apply=apply)


@app.route('/apply', methods=['POST'])
@login_required
@role_required('ogrenci')
def apply():
    existing = (
        Internship.query.filter_by(student_id=current_user.id)
        .filter(Internship.status.in_(['Onay Bekliyor', 'Onaylandı']))
        .order_by(Internship.id.desc())
        .first()
    )
    if existing:
        flash('Zaten aktif veya bekleyen bir staj başvurunuz var.', 'error')
        return redirect(url_for('dashboard'))

    company = request.form.get('company', '').strip()
    internship_type = request.form.get('type', 'Zorunlu')
    start_date = request.form.get('start', '')
    end_date = request.form.get('end', '')
    description = request.form.get('description', '').strip()

    if not company or not start_date:
        flash('Şirket adı ve başlangıç tarihi zorunludur.', 'error')
        return redirect(url_for('dashboard'))

    db.session.add(
        Internship(
            student_id=current_user.id,
            company_name=company,
            internship_type=internship_type,
            start_date=start_date,
            end_date=end_date or None,
            description=description or None,
            status='Onay Bekliyor',
        )
    )
    db.session.commit()
    flash('Staj başvurunuz danışmana iletildi.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/add_log', methods=['POST'])
@login_required
@role_required('ogrenci')
def add_log():
    content = request.form.get('content', '').strip()
    if not content:
        flash('Günlük içeriği boş olamaz.', 'error')
        return redirect(url_for('dashboard'))

    internship = Internship.query.filter_by(
        student_id=current_user.id, status='Onaylandı'
    ).first()
    if not internship:
        flash('Günlük eklemek için onaylanmış bir stajınız olmalı.', 'error')
        return redirect(url_for('dashboard'))

    db.session.add(
        DailyLog(
            student_id=current_user.id,
            student_name=current_user.name,
            content=content,
            status='Beklemede',
        )
    )
    db.session.commit()
    flash('Günlük kaydınız danışmana gönderildi.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/action/apply/<int:apply_id>/<action>', methods=['GET', 'POST'])
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
    return redirect(url_for('dashboard'))


@app.route('/action/log/<int:log_id>/<action>', methods=['GET', 'POST'])
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
    student_no = request.form.get('student_no', '').strip() or None
    department = request.form.get('department', '').strip() or None

    if not all([name, email, password]):
        flash('Tüm alanları doldurun.', 'error')
        return redirect(url_for('dashboard'))

    if role not in ('admin', 'danisman', 'ogrenci'):
        flash('Geçersiz rol.', 'error')
        return redirect(url_for('dashboard'))

    if User.query.filter_by(email=email).first():
        flash('Bu e-posta zaten kayıtlı.', 'error')
        return redirect(url_for('dashboard'))

    db.session.add(
        User(
            email=email,
            password=generate_password_hash(password),
            name=name,
            role=role,
            student_no=student_no,
            department=department,
        )
    )
    db.session.commit()
    flash(f'{name} sisteme eklendi.', 'success')
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


with app.app_context():
    init_database(app)


if __name__ == '__main__':
    app.run(debug=True)
