"""Veritabanini sifirlar ve demo verileri yukler."""
from app import app
from models import db
from db_seed import seed_demo_users, seed_sirketler

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_demo_users()
    seed_sirketler()
    print('Veritabani hazir.')
    print('Admin: admin@staj.edu.tr / admin123')
    print('Danisman: danisman@staj.edu.tr / danisman123')
    print('Ogrenci: ogr@staj.edu.tr / ogr123')
