# StajFlow - demo kullanicilar ve baslangic verileri
import os

from werkzeug.security import generate_password_hash

from models import db, User, Company, InternshipProgram, University

ROLE_MAP = {
    'student': 'ogrenci',
    'ogrenci': 'ogrenci',
    'öğrenci': 'ogrenci',
    'advisor': 'danisman',
    'danisman': 'danisman',
    'danışman': 'danisman',
    'danishman': 'danisman',
    'admin': 'admin',
    'yonetici': 'admin',
    'yönetici': 'admin',
}

DEMO_USERS = [
    ('admin@staj.edu.tr', 'admin123', 'Admin', 'admin', None, None),
    ('danisman@staj.edu.tr', 'danisman123', 'Dr. Ahmet Yılmaz', 'danisman', None, 'Bilgisayar Mühendisliği'),
    ('ogr@staj.edu.tr', 'ogr123', 'Ayşe Demir', 'ogrenci', '2021001001', 'Bilgisayar Mühendisliği'),
]


def normalize_role(role):
    if not role:
        return 'ogrenci'
    return ROLE_MAP.get(role.strip().lower(), role.strip().lower())


def is_danisman(role):
    return normalize_role(role) == 'danisman'


def default_university_name():
    return os.environ.get('UNIVERSITY_NAME', 'Üniversite Staj Yönetim Sistemi')


def seed_university():
    uni = University.query.first()
    if uni:
        return uni

    name = default_university_name()
    uni = University(
        name=name,
        short_name=name.split()[0] if name else 'Üniversite',
        domain='staj.edu.tr',
        city='Türkiye',
        is_active=True,
    )
    db.session.add(uni)
    db.session.commit()
    return uni


def ensure_demo_users():
    uni = seed_university()

    for email, sifre, isim, rol, no, bolum in DEMO_USERS:
        user = User.query.filter_by(email=email).first()
        if user:
            user.name = isim
            user.role = rol
            user.university_id = uni.id
            if no:
                user.student_no = no
            if bolum:
                user.department = bolum
        else:
            db.session.add(User(
                email=email,
                password=generate_password_hash(sifre),
                name=isim,
                role=rol,
                student_no=no,
                department=bolum,
                university_id=uni.id,
            ))

    # sifre unutulursa diye sadece demo maillerde sifreyi sabit tutuyoruz
    for email, sifre, *_ in DEMO_USERS:
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(sifre)
    ogr = User.query.filter_by(email='ogr@staj.edu.tr').first()
    if ogr:
        ogr.gpa = 3.42
        ogr.graduated_school = 'Anadolu Lisesi'
        ogr.experience = 'Freelance web projeleri, okul kulübü yazılım ekibi'
        ogr.foreign_language = 'İngilizce — B2'
    danisman = User.query.filter_by(email='danisman@staj.edu.tr').first()
    if danisman:
        danisman.title = 'Öğretim Üyesi'
    db.session.commit()


def seed_demo_users():
    ensure_demo_users()


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
            description='SQL ve raporlama çalışmaları.',
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
    user_cols = {
        'university_id': 'INTEGER',
        'title': 'VARCHAR(100)',
        'gpa': 'FLOAT',
        'graduated_school': 'VARCHAR(150)',
        'experience': 'TEXT',
        'foreign_language': 'VARCHAR(120)',
        'phone': 'VARCHAR(30)',
    }
    if 'user' in inspector.get_table_names():
        cols = {c['name'] for c in inspector.get_columns('user')}
        for col, typ in user_cols.items():
            if col not in cols:
                db.session.execute(text(f'ALTER TABLE user ADD COLUMN {col} {typ}'))
    if 'internship' in inspector.get_table_names():
        cols = {c['name'] for c in inspector.get_columns('internship')}
        if 'score' not in cols:
            db.session.execute(text('ALTER TABLE internship ADD COLUMN score INTEGER'))
        if 'advisor_note' not in cols:
            db.session.execute(text('ALTER TABLE internship ADD COLUMN advisor_note TEXT'))
        if 'created_at' not in cols:
            db.session.execute(text('ALTER TABLE internship ADD COLUMN created_at DATETIME'))
    if 'daily_log' in inspector.get_table_names():
        cols = {c['name'] for c in inspector.get_columns('daily_log')}
        if 'hours' not in cols:
            db.session.execute(text('ALTER TABLE daily_log ADD COLUMN hours INTEGER'))
    if 'internship_program' in inspector.get_table_names():
        cols = {c['name'] for c in inspector.get_columns('internship_program')}
        if 'created_at' not in cols:
            db.session.execute(text('ALTER TABLE internship_program ADD COLUMN created_at DATETIME'))
    db.session.commit()


def init_database(app):
    import os

    os.makedirs(app.instance_path, exist_ok=True)
    with app.app_context():
        db.create_all()
        _ensure_columns()
        seed_university()
        ensure_demo_users()
        seed_sirketler()
