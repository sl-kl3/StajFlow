from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, DailyLog, Internship
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'stajflow_full_power_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stajflow.db'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Bilgiler hatalı!')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('admin.html', users=User.query.all())
    elif current_user.role == 'danisman':
        logs = DailyLog.query.filter_by(status='Beklemede').all()
        applies = Internship.query.filter_by(status='Onay Bekliyor').all()
        return render_template('advisor.html', logs=logs, applies=applies)
    else:
        logs = DailyLog.query.filter_by(student_id=current_user.id).all()
        apply = Internship.query.filter_by(student_id=current_user.id).first()
        return render_template('student.html', logs=logs, apply=apply)

@app.route('/apply', methods=['POST'])
@login_required
def apply():
    new_apply = Internship(
        student_id=current_user.id,
        company_name=request.form.get('company'),
        internship_type=request.form.get('type'),
        start_date=request.form.get('start')
    )
    db.session.add(new_apply)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_log', methods=['POST'])
@login_required
def add_log():
    new_log = DailyLog(student_id=current_user.id, student_name=current_user.name, content=request.form.get('content'))
    db.session.add(new_log)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)