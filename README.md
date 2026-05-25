# StajFlow

Staj takip sistemi — **StajFlow (GitHub)** + **Staj Takip v3** + **HTML prototip** birleşimi.

## Roller

- **Öğrenci** — staj başvurusu, günlük kaydı
- **Danışman** — başvuru ve günlük onayı, istatistik paneli
- **Admin** — kullanıcı yönetimi

## Kurulum

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python setup_db.py
python app.py
```

http://127.0.0.1:5000

> İlk çalıştırmada `instance/stajflow.db` otomatik oluşur ve demo hesaplar eklenir.

## Demo giriş (danışman dahil)

| Rol | E-posta | Şifre |
|-----|---------|-------|
| Admin | admin@staj.edu.tr | admin123 |
| Danışman | hoca@staj.edu.tr | hoca123 |
| Danışman (v3) | ahmet@staj.edu.tr | dan123 |
| Öğrenci | ogr@staj.edu.tr | ogr123 |

## Git (ekip)

```bash
git pull origin main
git add .
git commit -m "aciklama"
git push origin main
```

https://github.com/sl-kl3/StajFlow
