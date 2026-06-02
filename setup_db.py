"""Veritabanını sıfırlar ve demo verileri yeniden kurar."""
from app import app
from models import db, User, Internship, DailyLog
from db_seed import ensure_demo_users, ensure_sample_data

with app.app_context():
    db.drop_all()
    db.create_all()
    ensure_demo_users()
    ensure_sample_data()
    print('Veritabani hazir.')
    print('Danisman: danisman@staj.edu.tr / danisman123')
