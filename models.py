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


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sector = db.Column(db.String(80), nullable=True)
    contact = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    programs = db.relationship('InternshipProgram', backref='company', lazy=True)


class InternshipProgram(db.Model):
    """Sirketin actigi staj ilani — ogrenci buradan secer."""
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    internship_type = db.Column(db.String(50), default='Zorunlu')
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50), nullable=True)
    quota = db.Column(db.Integer, default=5)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Internship', backref='program', lazy=True)


class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('internship_program.id'), nullable=True)
    company_name = db.Column(db.String(100), nullable=False)
    internship_type = db.Column(db.String(50), default='Zorunlu')
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Onay Bekliyor')
    score = db.Column(db.Integer, nullable=True)
    advisor_note = db.Column(db.Text, nullable=True)


class DailyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_name = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    hours = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default='Beklemede')