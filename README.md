# Rent A Car Otomasyonu

Bu proje, MySQL ve PyQt6 kullanılarak geliştirilmiş çok katmanlı (N-Tier) bir araç kiralama otomasyonudur.

## Kurulum ve Çalıştırma Adımları

**1. Gereksinimler ve Kütüphaneler:**
Terminali proje klasöründe açın ve gerekli kütüphaneleri yüklemek için şu komutu çalıştırın:
`pip install -r requirements.txt`

**2. Veritabanı Kurulumu:**
MySQL yönetim aracınızda (Workbench vb.) `final_odev.sql` dosyasını çalıştırarak tüm tabloları, prosedürleri, fonksiyonları ve trigger'ları otomatik olarak oluşturun.

**3. Çalıştırma:**
* Eğer MySQL 'root' kullanıcınızın şifresi **yoksa** direkt `python main.py` komutunu çalıştırın.
* Eğer MySQL şifreniz **varsa**, koda hiç dokunmadan kullandığınız terminale göre aşağıdaki komutlardan birini çalıştırın (sifreniz yazan yere kendi şifrenizi girin):
  - **PowerShell kullanıyorsanız:** `$env:MYSQL_PASS="sifreniz"; python main.py`
  - **CMD (Komut İstemi) kullanıyorsanız:** `set MYSQL_PASS=sifreniz && python main.py`