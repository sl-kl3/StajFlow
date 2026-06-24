# veritabani tablolari - Nazli
# user, company, internship vs hepsi burda tanimli

from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class University(db.Model):
    # uni adi falan, headerda gorunuyor
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    short_name = db.Column(db.String(40), nullable=True)
    domain = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    users = db.relationship('User', backref='university', lazy=True)


class User(UserMixin, db.Model):
    # ogrenci danisman admin hepsi bu tabloda, role alani ayiriyor
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    student_no = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=True)
    title = db.Column(db.String(100), nullable=True)
    gpa = db.Column(db.Float, nullable=True)
    graduated_school = db.Column(db.String(150), nullable=True)
    experience = db.Column(db.Text, nullable=True)
    foreign_language = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(30), nullable=True)

    internships = db.relationship('Internship', backref='student', lazy=True)
    daily_logs = db.relationship('DailyLog', backref='student', lazy=True)
    documents = db.relationship('StudentDocument', backref='student', lazy=True)


class StudentDocument(db.Model):
    # ogrencinin yukledigi cv diploma vs
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doc_type = db.Column(db.String(30), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    original_name = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sector = db.Column(db.String(80), nullable=True)
    contact = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    programs = db.relationship('InternshipProgram', backref='company', lazy=True)


class InternshipProgram(db.Model):
    # adminin actigi staj ilanlari
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
    # ogrenci basvurusu, status: Onay Bekliyor / Onaylandi / Reddedildi
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DailyLog(db.Model):
    # staj gunlugu
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_name = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    hours = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default='Beklemede')
