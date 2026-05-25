from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    student_no = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), nullable=False)

    internships = db.relationship('Internship', backref='student', lazy=True)
    daily_logs = db.relationship('DailyLog', backref='student', lazy=True)


class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    internship_type = db.Column(db.String(50), default='Zorunlu')
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Onay Bekliyor')


class DailyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_name = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Beklemede')
