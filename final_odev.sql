CREATE DATABASE abc_rentacar;
USE abc_rentacar;

-- Müşteriler Tablosu
CREATE TABLE musteriler (
    musteri_id VARCHAR(64) NOT NULL,
    tc_kimlik VARCHAR(11) UNIQUE NOT NULL,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    telefon VARCHAR(15) NOT NULL,
    ehliyet_no VARCHAR(20) NOT NULL,
    adres VARCHAR(250),
    PRIMARY KEY (musteri_id)
);

-- Araçlar Tablosu
CREATE TABLE araclar (
    arac_id VARCHAR(64) NOT NULL,
    plaka VARCHAR(20) UNIQUE NOT NULL,
    marka VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    yil INT CHECK (yil >= 2005),
    yakit_turu VARCHAR(20) NOT NULL,
    vites_turu VARCHAR(20) NOT NULL,
    gunluk_fiyat FLOAT NOT NULL,
    durum VARCHAR(20) DEFAULT 'Müsait',
    PRIMARY KEY (arac_id)
);

-- Kiralamalar Tablosu
CREATE TABLE kiralamalar (
    kiralama_id VARCHAR(64) NOT NULL,
    musteri_id VARCHAR(64) NOT NULL,
    arac_id VARCHAR(64) NOT NULL,
    kiralama_tarihi DATETIME NOT NULL,
    baslangic_tarihi DATE NOT NULL,
    bitis_tarihi DATE NOT NULL,
    toplam_tutar FLOAT NOT NULL,
    PRIMARY KEY (kiralama_id),
    FOREIGN KEY (musteri_id) REFERENCES musteriler(musteri_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (arac_id) REFERENCES araclar(arac_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Ödemeler Tablosu
CREATE TABLE odemeler (
    odeme_id VARCHAR(64) NOT NULL,
    musteri_id VARCHAR(64) NOT NULL,
    odeme_tarihi DATETIME NOT NULL,
    odeme_tutari FLOAT NOT NULL,
    odeme_turu VARCHAR(25) NOT NULL,
    aciklama VARCHAR(250),
    PRIMARY KEY (odeme_id),
    FOREIGN KEY (musteri_id) REFERENCES musteriler(musteri_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ==========================================
-- MÜŞTERİ İŞLEMLERİ
-- ==========================================

DELIMITER $$
CREATE PROCEDURE sp_MusteriListele ()
BEGIN
    SELECT * FROM musteriler;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_MusteriEkle (
    p_id VARCHAR(64), 
    p_tc VARCHAR(11), 
    p_ad VARCHAR(50), 
    p_soyad VARCHAR(50), 
    p_tel VARCHAR(15), 
    p_ehliyet VARCHAR(20), 
    p_adres VARCHAR(250)
)
BEGIN
    INSERT INTO musteriler VALUES (p_id, p_tc, p_ad, p_soyad, p_tel, p_ehliyet, p_adres);
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_MusteriGuncelle (
    p_id VARCHAR(64), 
    p_tc VARCHAR(11), 
    p_ad VARCHAR(50), 
    p_soyad VARCHAR(50), 
    p_tel VARCHAR(15), 
    p_ehliyet VARCHAR(20), 
    p_adres VARCHAR(250)
)
BEGIN
    UPDATE musteriler 
    SET tc_kimlik = p_tc, ad = p_ad, soyad = p_soyad, telefon = p_tel, ehliyet_no = p_ehliyet, adres = p_adres 
    WHERE musteri_id = p_id;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_MusteriSil (
    p_id VARCHAR(64)
)
BEGIN
    DELETE FROM musteriler 
    WHERE musteri_id = p_id;
END $$
DELIMITER ;

-- ==========================================
-- ARAÇ İŞLEMLERİ
-- ==========================================

DELIMITER $$
CREATE PROCEDURE sp_AracListele ()
BEGIN
    SELECT * FROM araclar;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_AracEkle (
    p_id VARCHAR(64), 
    p_plaka VARCHAR(20), 
    p_marka VARCHAR(50), 
    p_model VARCHAR(50), 
    p_yil INT, 
    p_yakit VARCHAR(20), 
    p_vites VARCHAR(20), 
    p_fiyat FLOAT
)
BEGIN
    INSERT INTO araclar (arac_id, plaka, marka, model, yil, yakit_turu, vites_turu, gunluk_fiyat) 
    VALUES (p_id, p_plaka, p_marka, p_model, p_yil, p_yakit, p_vites, p_fiyat);
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_AracGuncelle (
    p_id VARCHAR(64), 
    p_plaka VARCHAR(20), 
    p_marka VARCHAR(50), 
    p_model VARCHAR(50), 
    p_yil INT, 
    p_yakit VARCHAR(20), 
    p_vites VARCHAR(20), 
    p_fiyat FLOAT, 
    p_durum VARCHAR(20)
)
BEGIN
    UPDATE araclar 
    SET plaka = p_plaka, marka = p_marka, model = p_model, yil = p_yil, yakit_turu = p_yakit, vites_turu = p_vites, gunluk_fiyat = p_fiyat, durum = p_durum 
    WHERE arac_id = p_id;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_AracSil (
    p_id VARCHAR(64)
)
BEGIN
    DELETE FROM araclar 
    WHERE arac_id = p_id;
END $$
DELIMITER ;

-- ==========================================
-- KİRALAMA İŞLEMLERİ
-- ==========================================

DELIMITER $$
CREATE PROCEDURE sp_KiralamaListele ()
BEGIN
    SELECT 
        k.kiralama_id, 
        CONCAT(m.ad, ' ', m.soyad) AS Musteri, 
        a.plaka AS Arac_Plaka, 
        k.kiralama_tarihi, 
        k.baslangic_tarihi, 
        k.bitis_tarihi, 
        k.toplam_tutar 
    FROM kiralamalar k
    INNER JOIN musteriler m ON k.musteri_id = m.musteri_id
    INNER JOIN araclar a ON k.arac_id = a.arac_id;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_KiralamaEkle (
    p_id VARCHAR(64), 
    p_mid VARCHAR(64), 
    p_aid VARCHAR(64), 
    p_tarih DATETIME, 
    p_baslangic DATE, 
    p_bitis DATE, 
    p_tutar FLOAT
)
BEGIN
    INSERT INTO kiralamalar 
    VALUES (p_id, p_mid, p_aid, p_tarih, p_baslangic, p_bitis, p_tutar);
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_KiralamaGuncelle (
    p_id VARCHAR(64), 
    p_baslangic DATE, 
    p_bitis DATE, 
    p_tutar FLOAT
)
BEGIN
    UPDATE kiralamalar 
    SET baslangic_tarihi = p_baslangic, bitis_tarihi = p_bitis, toplam_tutar = p_tutar 
    WHERE kiralama_id = p_id;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_KiralamaSil (
    p_id VARCHAR(64)
)
BEGIN
    DELETE FROM kiralamalar 
    WHERE kiralama_id = p_id;
END $$
DELIMITER ;

-- ==========================================
-- ÖDEME İŞLEMLERİ
-- ==========================================

DELIMITER $$
CREATE PROCEDURE sp_OdemeListele ()
BEGIN
    SELECT 
        o.odeme_id, 
        CONCAT(m.ad, ' ', m.soyad) AS Musteri, 
        o.odeme_tarihi, 
        o.odeme_tutari, 
        o.odeme_turu, 
        o.aciklama
    FROM odemeler o
    INNER JOIN musteriler m ON o.musteri_id = m.musteri_id;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_OdemeEkle (
    p_id VARCHAR(64), 
    p_mid VARCHAR(64), 
    p_tarih DATETIME, 
    p_tutar FLOAT, 
    p_tur VARCHAR(25), 
    p_aciklama VARCHAR(250)
)
BEGIN
    INSERT INTO odemeler 
    VALUES (p_id, p_mid, p_tarih, p_tutar, p_tur, p_aciklama);
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_OdemeGuncelle (
    p_id VARCHAR(64), 
    p_tarih DATETIME, 
    p_tutar FLOAT, 
    p_tur VARCHAR(25), 
    p_aciklama VARCHAR(250)
)
BEGIN
    UPDATE odemeler 
    SET odeme_tarihi = p_tarih, odeme_tutari = p_tutar, odeme_turu = p_tur, aciklama = p_aciklama 
    WHERE odeme_id = p_id;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_OdemeSil (
    p_id VARCHAR(64)
)
BEGIN
    DELETE FROM odemeler 
    WHERE odeme_id = p_id;
END $$
DELIMITER ;

DELIMITER $$
CREATE FUNCTION fn_KiralamaGunSayisi(baslangic DATE, bitis DATE) 
RETURNS INT DETERMINISTIC
BEGIN
    DECLARE gun_sayisi INT;
    SET gun_sayisi = DATEDIFF(bitis, baslangic);
    IF gun_sayisi < 1 THEN
        SET gun_sayisi = 1; -- En az 1 günlük kiralama sayılır
    END IF;
    RETURN gun_sayisi;
END $$
DELIMITER ;


DELIMITER $$
CREATE FUNCTION fn_MusteriKalanBorc(p_musteri_id VARCHAR(64)) 
RETURNS FLOAT READS SQL DATA
BEGIN
    DECLARE toplam_borc FLOAT DEFAULT 0;
    DECLARE toplam_odenen FLOAT DEFAULT 0;
    
    SELECT IFNULL(SUM(toplam_tutar), 0) INTO toplam_borc 
    FROM kiralamalar 
    WHERE musteri_id = p_musteri_id;
    
    SELECT IFNULL(SUM(odeme_tutari), 0) INTO toplam_odenen 
    FROM odemeler 
    WHERE musteri_id = p_musteri_id;
    
    RETURN (toplam_borc - toplam_odenen);
END $$
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_AracDurumKirada 
AFTER INSERT ON kiralamalar 
FOR EACH ROW 
BEGIN
    UPDATE araclar 
    SET durum = 'Kirada' 
    WHERE arac_id = NEW.arac_id;
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER trg_KiralamaKontrol 
BEFORE INSERT ON kiralamalar 
FOR EACH ROW 
BEGIN
    DECLARE mevcut_durum VARCHAR(20);
    DECLARE hata_mesaji VARCHAR(250);
    
    SELECT durum INTO mevcut_durum 
    FROM araclar 
    WHERE arac_id = NEW.arac_id;
    
    IF mevcut_durum != 'Müsait' THEN
        SET hata_mesaji = 'HATA: Seçilen araç şu anda müsait değil, kiralama yapılamaz!';
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = hata_mesaji;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_KiralamaIptal 
AFTER DELETE ON kiralamalar 
FOR EACH ROW 
BEGIN
    UPDATE araclar 
    SET durum = 'Müsait' 
    WHERE arac_id = OLD.arac_id;
END //
DELIMITER ;