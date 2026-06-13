# Arayuz (UI) Notlari

**Modul sahibi:** Ilknur  
**Dosyalar:** `templates/base.html`, `templates/login.html`, `static/css/style.css`, `templates/danisman/*`

---

## Ne yaptik?

Kullanicinin gordugu kisim bizde. Renkler, menu, login ekrani, danisman sayfalarinin gorunumu.

## UI ne demek?

**UI = User Interface = Kullanici arayuzu**

Butonlar, renkler, sol menu (sidebar), kartlar — hepsi UI.

## Onemli dosyalar

| Dosya | Gorev |
|-------|-------|
| base.html | Ortak sablon, sol menu, header |
| login.html | Giris ekrani |
| style.css | Tum renk ve duzen |
| danisman/*.html | Danisman paneli ekranlari (4 sayfa) |

## Menu rol bazli nasil degisiyor?

`base.html` icinde:

- Ogrenci girerse → ogrenci linkleri
- Danisman girerse → danisman linkleri
- Admin girerse → admin linkleri

## Sunumda gosterilecek

1. Login ekrani
2. 3 farkli rolde sol menu farki
3. Danisman basvuru onay ekrani

---

*Hazirlayan: (buraya adini yaz - ornek: Ilknur Demir)*  
*Tarih: (bugunun tarihi)*
