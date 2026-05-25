"""Demo kullanıcı ve örnek veri — mevcut veriyi silmeden eksikleri tamamlar."""
from werkzeug.security import generate_password_hash

from models import db, User, Internship, DailyLog

ROLE_ALIASES = {
    'danishman': 'danisman',
    'danisman': 'danisman',
    'advisor': 'danisman',
    'ogrenci': 'ogrenci',
    'student': 'ogrenci',
    'admin': 'admin',
}

DEMO_USERS = [
    ('admin@staj.edu.tr', 'admin123', 'Sistem Yöneticisi', 'admin'),
    ('hoca@staj.edu.tr', 'hoca123', 'Dr. Ahmet Yılmaz', 'danisman'),
    ('ahmet@staj.edu.tr', 'dan123', 'Ahmet Yıldız', 'danisman'),
    ('ogr@staj.edu.tr', 'ogr123', 'Ayşe Demir', 'ogrenci'),
    ('ayse@ogrenci.edu.tr', 'ogr123', 'Ayşe Yılmaz', 'ogrenci'),
    ('ali@staj.edu.tr', 'ali123', 'Ali Kaya', 'ogrenci'),
    ('mehmet@ogrenci.edu.tr', 'ogr123', 'Mehmet Demir', 'ogrenci'),
]


def normalize_role(role):
    if not role:
        return 'ogrenci'
    return ROLE_ALIASES.get(role.strip().lower(), role.strip().lower())


def is_danisman(role):
    return normalize_role(role) == 'danisman'


def ensure_demo_users():
    """Demo hesapları oluşturur veya şifre/rolünü düzeltir."""
    changed = False
    for email, pwd, name, role in DEMO_USERS:
        role = normalize_role(role)
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                password=generate_password_hash(pwd),
                name=name,
                role=role,
            )
            db.session.add(user)
            changed = True
        else:
            user.password = generate_password_hash(pwd)
            user.name = name
            if normalize_role(user.role) != role:
                user.role = role
                changed = True
    if changed:
        db.session.commit()

    # Eski yanlış rol yazımlarını düzelt
    for user in User.query.all():
        fixed = normalize_role(user.role)
        if user.role != fixed:
            user.role = fixed
            changed = True
    if changed:
        db.session.commit()


def ensure_sample_data():
    """Örnek başvuru ve günlük yoksa ekle."""
    for email, no, dept in (
        ('ogr@staj.edu.tr', '2021001001', 'Bilgisayar Mühendisliği'),
        ('ayse@ogrenci.edu.tr', '2021001001', 'Bilgisayar Mühendisliği'),
        ('ali@staj.edu.tr', '2021001002', 'Bilgisayar Mühendisliği'),
        ('mehmet@ogrenci.edu.tr', '2021001003', 'Bilgisayar Mühendisliği'),
    ):
        u = User.query.filter_by(email=email).first()
        if u and not u.student_no:
            u.student_no = no
            u.department = dept

    ogr = User.query.filter_by(email='ogr@staj.edu.tr').first()
    ali = User.query.filter_by(email='ali@staj.edu.tr').first()
    if not ogr:
        db.session.commit()
        return

    if not Internship.query.filter_by(student_id=ogr.id).first():
        db.session.add(
            Internship(
                student_id=ogr.id,
                company_name='Anadolu Yazılım A.Ş.',
                internship_type='Zorunlu',
                start_date='2026-06-01',
                end_date='2026-08-31',
                description='Backend geliştirme stajı',
                status='Onaylandı',
            )
        )

    if ali and not Internship.query.filter_by(student_id=ali.id).first():
        db.session.add(
            Internship(
                student_id=ali.id,
                company_name='Tekno A.Ş.',
                internship_type='Gönüllü',
                start_date='2026-07-15',
                description='Frontend staj başvurusu',
                status='Onay Bekliyor',
            )
        )

    if not DailyLog.query.filter_by(student_id=ogr.id).first():
        db.session.add(
            DailyLog(
                student_id=ogr.id,
                student_name=ogr.name,
                content='Proje ortamı kuruldu, ekip ile tanışma toplantısı yapıldı.',
                status='Beklemede',
            )
        )
        db.session.add(
            DailyLog(
                student_id=ogr.id,
                student_name=ogr.name,
                content='İlk sprint görevleri tamamlandı, kod incelemesi alındı.',
                status='Onaylandı',
            )
        )

    db.session.commit()


def _schema_ok(db):
    from sqlalchemy import inspect

    insp = inspect(db.engine)
    if not insp.has_table('user'):
        return False
    cols = {c['name'] for c in insp.get_columns('user')}
    if not {'student_no', 'department'}.issubset(cols):
        return False
    if insp.has_table('internship'):
        icols = {c['name'] for c in insp.get_columns('internship')}
        if not {'end_date', 'description'}.issubset(icols):
            return False
    return True


def init_database(app):
    import os
    from models import db

    os.makedirs(app.instance_path, exist_ok=True)
    with app.app_context():
        if not _schema_ok(db):
            db.drop_all()
        db.create_all()
        ensure_demo_users()
        ensure_sample_data()
