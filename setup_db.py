from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all() # Her şeyi sıfırla
    db.create_all() # Yeni tabloları kur
    
    users = [
        ("admin@staj.edu.tr", "admin123", "Sistem Yöneticisi", "admin"),
        ("hoca@staj.edu.tr", "hoca123", "Dr. Ahmet Yılmaz", "danisman"),
        ("ogr@staj.edu.tr", "ogr123", "Ayşe Demir", "ogrenci")
    ]
    
    for email, pwd, name, role in users:
        hashed_password = generate_password_hash(pwd)
        db.session.add(User(email=email, password=hashed_password, name=name, role=role))
    
    db.session.commit()
    print("🚀 SİSTEM SIFIRLANDI VE YENİDEN KURULDU!")