# StajFlow

Üniversite staj takip sistemi — hocaya sunum için demo hesaplarla çalışır.

## Akış

1. **Admin** — şirket ekler, staj programı açar (şirket adına)
2. **Öğrenci** — açık programlardan birini seçer, başvurur
3. **Danışman** — başvuruyu onaylar/reddeder
4. **Öğrenci** — onay sonrası günlük kaydı girer
5. **Danışman** — günlükleri onaylar

## Demo hesaplar (3 tane yeter)

| Rol | E-posta | Şifre |
|-----|---------|-------|
| Admin | admin@staj.edu.tr | admin123 |
| Danışman | hoca@staj.edu.tr | hoca123 |
| Öğrenci | ogr@staj.edu.tr | ogr123 |

## Kurulum

```bash
pip install -r requirements.txt
python setup_db.py
python app.py
```

http://127.0.0.1:5000

## Hocaya gösterim sırası

1. Admin → 3 şirket + programlar (zaten demo veride var)
2. Öğrenci → program seç → başvuru
3. Danışman → başvuru onay → günlük onay
