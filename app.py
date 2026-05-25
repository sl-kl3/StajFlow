import os
from functools import wraps

from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, DailyLog, Internship
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'stajflow_full_power_123')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///stajflow.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                flash('Bu işlem için yetkiniz yok.')
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
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
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
    if current_user.role == 'admin':
        users = User.query.order_by(User.role, User.name).all()
        stats = {
            'total': len(users),
            'ogrenci': User.query.filter_by(role='ogrenci').count(),
            'danisman': User.query.filter_by(role='danisman').count(),
            'bekleyen_basvuru': Internship.query.filter_by(status='Onay Bekliyor').count(),
            'bekleyen_gunluk': DailyLog.query.filter_by(status='Beklemede').count(),
        }
        return render_template('admin.html', users=users, stats=stats)

    if current_user.role == 'danisman':
        logs = DailyLog.query.filter_by(status='Beklemede').order_by(DailyLog.date.desc()).all()
        applies = Internship.query.filter_by(status='Onay Bekliyor').order_by(Internship.id.desc()).all()
        approved_logs = DailyLog.query.filter(DailyLog.status != 'Beklemede').order_by(
            DailyLog.date.desc()
        ).limit(10).all()
        return render_template(
            'advisor.html',
            logs=logs,
            applies=applies,
            approved_logs=approved_logs,
        )

    logs = DailyLog.query.filter_by(student_id=current_user.id).order_by(
        DailyLog.date.desc()
    ).all()
    apply = Internship.query.filter_by(student_id=current_user.id).order_by(
        Internship.id.desc()
    ).first()
    return render_template('student.html', logs=logs, apply=apply)


@app.route('/apply', methods=['POST'])
@login_required
@role_required('ogrenci')
def apply():
    existing = Internship.query.filter_by(student_id=current_user.id).filter(
        Internship.status.in_(['Onay Bekliyor', 'Onaylandı'])
    ).order_by(Internship.id.desc()).first()
    if existing:
        flash('Zaten aktif veya bekleyen bir staj başvurunuz var.', 'error')
        return redirect(url_for('dashboard'))

    company = request.form.get('company', '').strip()
    internship_type = request.form.get('type', 'Zorunlu')
    start_date = request.form.get('start', '')

    if not company or not start_date:
        flash('Şirket adı ve başlangıç tarihi zorunludur.', 'error')
        return redirect(url_for('dashboard'))

    new_apply = Internship(
        student_id=current_user.id,
        company_name=company,
        internship_type=internship_type,
        start_date=start_date,
        status='Onay Bekliyor',
    )
    db.session.add(new_apply)
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

    new_log = DailyLog(
        student_id=current_user.id,
        student_name=current_user.name,
        content=content,
        status='Beklemede',
    )
    db.session.add(new_log)
    db.session.commit()
    flash('Günlük kaydınız danışmana gönderildi.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/action/apply/<int:apply_id>/<action>')
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


@app.route('/action/log/<int:log_id>/<action>')
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
    role = request.form.get('role', 'ogrenci')

    if not all([name, email, password]):
        flash('Tüm alanları doldurun.', 'error')
        return redirect(url_for('dashboard'))

    if role not in ('admin', 'danisman', 'ogrenci'):
        flash('Geçersiz rol.', 'error')
        return redirect(url_for('dashboard'))

    if User.query.filter_by(email=email).first():
        flash('Bu e-posta zaten kayıtlı.', 'error')
        return redirect(url_for('dashboard'))

    user = User(
        email=email,
        password=generate_password_hash(password),
        name=name,
        role=role,
    )
    db.session.add(user)
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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
