"""Veritabanını sıfırlar ve demo kullanıcı + örnek verileri ekler."""
from app import app, db
from models import User, Internship, DailyLog
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    users = [
        ("admin@staj.edu.tr", "admin123", "Sistem Yöneticisi", "admin"),
        ("hoca@staj.edu.tr", "hoca123", "Dr. Ahmet Yılmaz", "danisman"),
        ("ogr@staj.edu.tr", "ogr123", "Ayşe Demir", "ogrenci"),
        ("ali@staj.edu.tr", "ali123", "Ali Kaya", "ogrenci"),
    ]

    created = {}
    for email, pwd, name, role in users:
        user = User(
            email=email,
            password=generate_password_hash(pwd),
            name=name,
            role=role,
        )
        db.session.add(user)
        db.session.flush()
        created[email] = user

    ogr = created["ogr@staj.edu.tr"]
    ali = created["ali@staj.edu.tr"]

    db.session.add(
        Internship(
            student_id=ogr.id,
            company_name="Tech A.Ş.",
            internship_type="Zorunlu",
            start_date="2026-06-01",
            status="Onaylandı",
        )
    )
    db.session.add(
        Internship(
            student_id=ali.id,
            company_name="Yazılım Ltd.",
            internship_type="Gönüllü",
            start_date="2026-07-15",
            status="Onay Bekliyor",
        )
    )

    db.session.add(
        DailyLog(
            student_id=ogr.id,
            student_name=ogr.name,
            content="Proje ortamı kuruldu, ekip ile tanışma toplantısı yapıldı.",
            status="Beklemede",
        )
    )
    db.session.add(
        DailyLog(
            student_id=ogr.id,
            student_name=ogr.name,
            content="İlk sprint görevleri tamamlandı, kod incelemesi alındı.",
            status="Onaylandı",
        )
    )

    db.session.commit()
    print("Veritabani hazir. Demo hesaplar login ekraninda.")
