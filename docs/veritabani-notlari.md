# Veritabani Notlari

**Modul sahibi:** Nazli  
**Dosyalar:** `models.py`, `db_seed.py`, `setup_db.py`

---

## Ne yaptik?

StajFlow'da tum bilgiler veritabaninda tutuluyor. Biz Excel gibi tablolar kullandik.

## Tablolar (7 tane)

| Tablo | Ne tutuyor |
|-------|------------|
| user | Ogrenci, danisman, admin kullanicilari |
| university | Kurum adi |
| company | Staj sirketleri |
| internship_program | Staj ilanlari, kontenjan |
| internship | Ogrenci basvurulari, durum, puan |
| daily_log | Staj gunlukleri, calisilan saat |
| student_document | Yuklenen CV, diploma vb. |

## Iliskiler (basit)

- Bir ogrenci birden fazla basvuru yapabilir (ama ayni anda aktif basvuru sinirlidir)
- Bir sirketin birden fazla staj ilani olabilir
- Bir basvurunun gunlukleri ogrenci uzerinden baglanir

## Demo veri

`db_seed.py` icinde 3 demo hesap ve 3 sirket + 3 ilan var.

## Sunum oncesi

```bash
python setup_db.py
```

Temiz demo veri yukler.

---

*Hazirlayan: (buraya adini yaz - ornek: Nazli Yilmaz)*  
*Tarih: (bugunun tarihi)*
