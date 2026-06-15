# veritabanini sifirlar, sunumdan once bir kez calistir
from app import app
from models import db
from db_seed import ensure_demo_users, seed_sirketler, seed_university

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_university()
    ensure_demo_users()
    seed_sirketler()
    print('tamam, db hazir')
    print('admin@staj.edu.tr / admin123')
    print('danisman@staj.edu.tr / danisman123')
    print('ogr@staj.edu.tr / ogr123')
