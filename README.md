# StajFlow

Üniversite staj sürecini yöneten web uygulaması: **admin**, **danışman** ve **öğrenci** rolleri.

## Özellikler

- **Öğrenci:** Staj başvurusu, onay sonrası günlük kaydı, durum takibi
- **Danışman:** Başvuru ve günlük onay/red
- **Admin:** Kullanıcı ekleme/silme, sistem istatistikleri

## Kurulum

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python setup_db.py
python app.py
```

Tarayıcı: http://127.0.0.1:5000

## Demo hesaplar

| Rol | E-posta | Şifre |
|-----|---------|-------|
| Admin | admin@staj.edu.tr | admin123 |
| Danışman | hoca@staj.edu.tr | hoca123 |
| Öğrenci | ogr@staj.edu.tr | ogr123 |

## GitHub

```bash
git pull origin main
# degisikliklerden sonra
git add .
git commit -m "mesaj"
git push origin main
```

Repo: https://github.com/sl-kl3/StajFlow
