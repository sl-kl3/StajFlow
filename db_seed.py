# StajFlow - demo kullanicilar ve baslangic verileri
from werkzeug.security import generate_password_hash

from models import db, User, Company, InternshipProgram

# farkli yazilmis rolleri duzeltmek icin
ROLE_MAP = {
    'student': 'ogrenci',
    'ogrenci': 'ogrenci',
    'advisor': 'danisman',
    'danisman': 'danisman',
    'admin': 'admin',
}

DEMO_USERS = [
    ('admin@staj.edu.tr', 'admin123', 'Admin', 'admin'),
    ('danisman@staj.edu.tr', 'danisman123', 'Dr. Ahmet Yılmaz', 'danisman'),
    ('ogr@staj.edu.tr', 'ogr123', 'Ayşe Demir', 'ogrenci'),
]


def normalize_role(role):
    if not role:
        return 'ogrenci'
    return ROLE_MAP.get(role.strip().lower(), role.strip().lower())


def is_danisman(role):
    return normalize_role(role) == 'danisman'


def seed_demo_users():
    if User.query.first():
        return

    for email, sifre, isim, rol in DEMO_USERS:
        db.session.add(User(
            email=email,
            password=generate_password_hash(sifre),
            name=isim,
            role=rol,
        ))
    db.session.commit()

    ogr = User.query.filter_by(email='ogr@staj.edu.tr').first()
    if ogr:
        ogr.student_no = '2021001001'
        ogr.department = 'Bilgisayar Mühendisliği'
        db.session.commit()


def seed_sirketler():
    if Company.query.first():
        return

    sirketler = [
        Company(name='Anadolu Yazılım A.Ş.', sector='Yazılım', contact='info@anadolu.com', address='İstanbul'),
        Company(name='Tekno A.Ş.', sector='Teknoloji', contact='hr@tekno.com', address='Ankara'),
        Company(name='DataHub Ltd.', sector='Veri Bilimi', contact='staj@datahub.com', address='İzmir'),
    ]
    db.session.add_all(sirketler)
    db.session.flush()

    ilanlar = [
        InternshipProgram(
            company_id=sirketler[0].id,
            title='Backend Geliştirme Stajı',
            description='Python/Flask ile API geliştirme.',
            internship_type='Zorunlu',
            start_date='2026-06-01',
            end_date='2026-08-31',
            quota=3,
        ),
        InternshipProgram(
            company_id=sirketler[1].id,
            title='Frontend Staj Programı',
            description='React arayüz geliştirme.',
            internship_type='Gönüllü',
            start_date='2026-07-01',
            end_date='2026-09-30',
            quota=2,
        ),
        InternshipProgram(
            company_id=sirketler[2].id,
            title='Veri Analizi Stajı',
            description='SQL ve raporlama calismalari.',
            internship_type='Zorunlu',
            start_date='2026-06-15',
            end_date='2026-08-15',
            quota=2,
        ),
    ]
    db.session.add_all(ilanlar)
    db.session.commit()


def _ensure_columns():
    """Eski veritabanlarina eksik sutunlari ekler (SQLite)."""
    from sqlalchemy import inspect, text

    inspector = inspect(db.engine)
    if 'internship' in inspector.get_table_names():
        cols = {c['name'] for c in inspector.get_columns('internship')}
        if 'score' not in cols:
            db.session.execute(text('ALTER TABLE internship ADD COLUMN score INTEGER'))
        if 'advisor_note' not in cols:
            db.session.execute(text('ALTER TABLE internship ADD COLUMN advisor_note TEXT'))
    if 'daily_log' in inspector.get_table_names():
        cols = {c['name'] for c in inspector.get_columns('daily_log')}
        if 'hours' not in cols:
            db.session.execute(text('ALTER TABLE daily_log ADD COLUMN hours INTEGER'))
    db.session.commit()


def init_database(app):
    import os

    os.makedirs(app.instance_path, exist_ok=True)
    with app.app_context():
        db.create_all()
        _ensure_columns()
        seed_demo_users()
        seed_sirketler()
