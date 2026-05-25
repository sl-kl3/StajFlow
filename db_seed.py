"""Demo kullanıcı, şirket, staj programı ve örnek veriler."""
from werkzeug.security import generate_password_hash

from models import db, User, Company, InternshipProgram, Internship, DailyLog

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
    ('ogr@staj.edu.tr', 'ogr123', 'Ayşe Demir', 'ogrenci'),
]

LEGACY_REMOVE_EMAILS = (
    'ahmet@staj.edu.tr',
    'ayse@ogrenci.edu.tr',
    'mehmet@ogrenci.edu.tr',
    'ali@staj.edu.tr',
)


def normalize_role(role):
    if not role:
        return 'ogrenci'
    return ROLE_ALIASES.get(role.strip().lower(), role.strip().lower())


def is_danisman(role):
    return normalize_role(role) == 'danisman'


def remove_legacy_users():
    for email in LEGACY_REMOVE_EMAILS:
        user = User.query.filter_by(email=email).first()
        if not user:
            continue
        DailyLog.query.filter_by(student_id=user.id).delete()
        Internship.query.filter_by(student_id=user.id).delete()
        db.session.delete(user)
    db.session.commit()


def ensure_demo_users():
    remove_legacy_users()
    changed = False
    for email, pwd, name, role in DEMO_USERS:
        role = normalize_role(role)
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(
                email=email,
                password=generate_password_hash(pwd),
                name=name,
                role=role,
            ))
            changed = True
        else:
            user.password = generate_password_hash(pwd)
            user.name = name
            user.role = role
    if changed:
        db.session.commit()

    for user in User.query.all():
        fixed = normalize_role(user.role)
        if user.role != fixed:
            user.role = fixed
    db.session.commit()


def ensure_companies_and_programs():
    if Company.query.first():
        return

    c1 = Company(name='Anadolu Yazılım A.Ş.', sector='Yazılım', contact='info@anadolu.com', address='İstanbul')
    c2 = Company(name='Tekno A.Ş.', sector='Teknoloji', contact='hr@tekno.com', address='Ankara')
    c3 = Company(name='DataHub Ltd.', sector='Veri Bilimi', contact='staj@datahub.com', address='İzmir')
    db.session.add_all([c1, c2, c3])
    db.session.flush()

    programs = [
        InternshipProgram(
            company_id=c1.id,
            title='Backend Geliştirme Stajı',
            description='Python/Flask ile API geliştirme, ekip çalışması.',
            internship_type='Zorunlu',
            start_date='2026-06-01',
            end_date='2026-08-31',
            quota=3,
        ),
        InternshipProgram(
            company_id=c2.id,
            title='Frontend Staj Programı',
            description='React arayüz geliştirme ve UI testleri.',
            internship_type='Gönüllü',
            start_date='2026-07-01',
            end_date='2026-09-30',
            quota=2,
        ),
        InternshipProgram(
            company_id=c3.id,
            title='Veri Analizi Stajı',
            description='SQL, raporlama ve dashboard çalışmaları.',
            internship_type='Zorunlu',
            start_date='2026-06-15',
            end_date='2026-08-15',
            quota=2,
        ),
    ]
    db.session.add_all(programs)
    db.session.commit()


def ensure_sample_data():
    ogr = User.query.filter_by(email='ogr@staj.edu.tr').first()
    if not ogr:
        return
    if not ogr.student_no:
        ogr.student_no = '2021001001'
        ogr.department = 'Bilgisayar Mühendisliği'

    prog = InternshipProgram.query.filter_by(title='Backend Geliştirme Stajı').first()
    if prog and not Internship.query.filter_by(student_id=ogr.id).first():
        db.session.add(Internship(
            student_id=ogr.id,
            program_id=prog.id,
            company_name=prog.company.name,
            internship_type=prog.internship_type,
            start_date=prog.start_date,
            end_date=prog.end_date,
            description=prog.description,
            status='Onaylandı',
        ))

    if not DailyLog.query.filter_by(student_id=ogr.id).first():
        db.session.add(DailyLog(
            student_id=ogr.id,
            student_name=ogr.name,
            content='Proje ortamı kuruldu, ekip ile tanışma toplantısı yapıldı.',
            status='Beklemede',
        ))
        db.session.add(DailyLog(
            student_id=ogr.id,
            student_name=ogr.name,
            content='İlk sprint görevleri tamamlandı.',
            status='Onaylandı',
        ))

    db.session.commit()


def _schema_ok(db):
    from sqlalchemy import inspect

    insp = inspect(db.engine)
    if not insp.has_table('user'):
        return False
    ucols = {c['name'] for c in insp.get_columns('user')}
    if not {'student_no', 'department'}.issubset(ucols):
        return False
    if not insp.has_table('company'):
        return False
    if not insp.has_table('internship_program'):
        return False
    if insp.has_table('internship'):
        icols = {c['name'] for c in insp.get_columns('internship')}
        if not {'program_id', 'end_date', 'description'}.issubset(icols):
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
        ensure_companies_and_programs()
        ensure_sample_data()
