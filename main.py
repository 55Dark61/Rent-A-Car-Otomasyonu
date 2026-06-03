import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
                             QLineEdit, QMessageBox, QHeaderView, QTabWidget, QComboBox, QDateEdit, QLabel)
from PyQt6.QtCore import QDate
from bll import BusinessLogicLayer

class RentACarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ABC Rent A Car - Yönetim Paneli")
        self.setGeometry(100, 100, 1200, 700)
        
        self.bll = BusinessLogicLayer()
        self.sekmeler = QTabWidget()
        self.setCentralWidget(self.sekmeler)
        
        self.sekme_musteri = QWidget()
        self.sekme_arac = QWidget()
        self.sekme_kiralama = QWidget()
        self.sekme_odeme = QWidget()
        
        self.sekmeler.addTab(self.sekme_musteri, "Müşteri Yönetimi")
        self.sekmeler.addTab(self.sekme_arac, "Araç Yönetimi")
        self.sekmeler.addTab(self.sekme_kiralama, "Kiralamalar")
        self.sekmeler.addTab(self.sekme_odeme, "Ödemeler")
        
        self.init_musteri_arayuz()
        self.init_arac_arayuz()
        self.init_kiralama_arayuz()
        self.init_odeme_arayuz()
        
        self.verileri_guncelle()

    def verileri_guncelle(self):
        self.musterileri_getir()
        self.araclari_getir()
        self.kiralamalari_getir()
        self.odemeleri_getir()
        self.acilir_listeleri_doldur()

    def acilir_listeleri_doldur(self):
        self.cmb_k_musteri.blockSignals(True)
        self.cmb_k_arac.blockSignals(True)
        self.cmb_o_kiralama.blockSignals(True)
        
        self.cmb_k_musteri.clear()
        self.cmb_o_kiralama.clear()
        
        # Müşterileri çekiyoruz ve isimlerinden ID bulmak için bir sözlük oluşturuyoruz
        musteriler = self.bll.musteri_listele()
        musteri_sozluk = {}
        if musteriler:
            for m in musteriler:
                isim = f"{m['ad']} {m['soyad']}"
                gorunen_isim = f"{isim} ({m['tc_kimlik']})"
                self.cmb_k_musteri.addItem(gorunen_isim, m['musteri_id'])
                musteri_sozluk[isim] = m['musteri_id']
                
        # Kiralamaları çekip Ödeme sayfasına ekliyoruz
        kiralamalar = self.bll.kiralama_listele()
        if kiralamalar:
            for k in kiralamalar:
                m_id = musteri_sozluk.get(k['Musteri'])
                if m_id: # Müşteri eşleşiyorsa ekle
                    bilgi = f"{k['Musteri']} - Plaka: {k['Arac_Plaka']} - {k['toplam_tutar']} TL"
                    # Arka planda ID'leri saklıyoruz
                    self.cmb_o_kiralama.addItem(bilgi, (k['kiralama_id'], m_id, k['toplam_tutar']))
                    
        self.cmb_o_kiralama.blockSignals(False)
        self.odeme_kiralama_secildi() # Seçimi güncelle

        self.cmb_k_arac.clear()
        araclar = self.bll.arac_listele()
        if araclar:
            for a in araclar:
                if a['durum'] == 'Müsait':
                    bilgi = f"{a['plaka']} - {a['marka']} {a['model']} ({a['gunluk_fiyat']} TL/Gün)"
                    self.cmb_k_arac.addItem(bilgi, (a['arac_id'], a['gunluk_fiyat']))
                    
        self.cmb_k_arac.blockSignals(False)
        self.cmb_k_musteri.blockSignals(False)
        self.kiralama_tutar_hesapla() 

    # ================= MÜŞTERİ SEKME =================
    def init_musteri_arayuz(self):
        layout = QVBoxLayout(self.sekme_musteri)
        form_layout = QHBoxLayout()
        self.txt_tc = QLineEdit(); self.txt_tc.setPlaceholderText("TC Kimlik")
        self.txt_tc.setMaxLength(11)
        self.txt_ad = QLineEdit(); self.txt_ad.setPlaceholderText("Ad")
        self.txt_soyad = QLineEdit(); self.txt_soyad.setPlaceholderText("Soyad")
        self.txt_tel = QLineEdit(); self.txt_tel.setPlaceholderText("Telefon")
        self.txt_ehliyet = QLineEdit(); self.txt_ehliyet.setPlaceholderText("Ehliyet No")
        self.txt_adres = QLineEdit(); self.txt_adres.setPlaceholderText("Adres")
        
        btn_ekle = QPushButton("Müşteri Ekle"); btn_ekle.clicked.connect(self.musteri_ekle_click)
        for w in [self.txt_tc, self.txt_ad, self.txt_soyad, self.txt_tel, self.txt_ehliyet, self.txt_adres, btn_ekle]:
            form_layout.addWidget(w)
        layout.addLayout(form_layout)

        buton_layout = QHBoxLayout()
        btn_yenile = QPushButton("Listeyi Yenile"); btn_yenile.clicked.connect(self.verileri_guncelle)
        btn_sil = QPushButton("Seçili Müşteriyi Sil"); btn_sil.clicked.connect(self.musteri_sil_click)
        buton_layout.addWidget(btn_yenile); buton_layout.addWidget(btn_sil)
        layout.addLayout(buton_layout)

        self.tablo_musteri = QTableWidget()
        self.tablo_musteri.setColumnCount(7)
        self.tablo_musteri.setHorizontalHeaderLabels(["Müşteri ID", "TC Kimlik", "Ad", "Soyad", "Telefon", "Ehliyet No", "Adres"])
        self.tablo_musteri.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tablo_musteri.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.tablo_musteri)

    def musterileri_getir(self):
        self.tablo_musteri.setRowCount(0)
        musteriler = self.bll.musteri_listele()
        if musteriler:
            for i, musteri in enumerate(musteriler):
                self.tablo_musteri.insertRow(i)
                self.tablo_musteri.setItem(i, 0, QTableWidgetItem(str(musteri['musteri_id'])))
                self.tablo_musteri.setItem(i, 1, QTableWidgetItem(str(musteri['tc_kimlik'])))
                self.tablo_musteri.setItem(i, 2, QTableWidgetItem(str(musteri['ad'])))
                self.tablo_musteri.setItem(i, 3, QTableWidgetItem(str(musteri['soyad'])))
                self.tablo_musteri.setItem(i, 4, QTableWidgetItem(str(musteri['telefon'])))
                self.tablo_musteri.setItem(i, 5, QTableWidgetItem(str(musteri['ehliyet_no'])))
                self.tablo_musteri.setItem(i, 6, QTableWidgetItem(str(musteri['adres'])))

    def musteri_ekle_click(self):
        tc, ad, soyad = self.txt_tc.text(), self.txt_ad.text(), self.txt_soyad.text()
        tel, ehliyet, adres = self.txt_tel.text(), self.txt_ehliyet.text(), self.txt_adres.text()
        if not all([tc, ad, soyad, tel, ehliyet]): return
        self.bll.musteri_ekle(tc, ad, soyad, tel, ehliyet, adres)
        self.verileri_guncelle()
        for box in [self.txt_tc, self.txt_ad, self.txt_soyad, self.txt_tel, self.txt_ehliyet, self.txt_adres]: box.clear()

    def musteri_sil_click(self):
        secili = self.tablo_musteri.currentRow()
        if secili >= 0:
            self.bll.musteri_sil(self.tablo_musteri.item(secili, 0).text())
            self.verileri_guncelle()

    # ================= ARAÇ SEKME =================
    def init_arac_arayuz(self):
        layout = QVBoxLayout(self.sekme_arac)
        form_layout = QHBoxLayout()
        self.txt_plaka = QLineEdit(); self.txt_plaka.setPlaceholderText("Plaka")
        self.txt_marka = QLineEdit(); self.txt_marka.setPlaceholderText("Marka")
        self.txt_model = QLineEdit(); self.txt_model.setPlaceholderText("Model")
        self.txt_yil = QLineEdit(); self.txt_yil.setPlaceholderText("Yıl")
        self.txt_yakit = QLineEdit(); self.txt_yakit.setPlaceholderText("Yakıt")
        self.txt_vites = QLineEdit(); self.txt_vites.setPlaceholderText("Vites")
        self.txt_fiyat = QLineEdit(); self.txt_fiyat.setPlaceholderText("Günlük Fiyat")
        
        btn_ekle = QPushButton("Araç Ekle"); btn_ekle.clicked.connect(self.arac_ekle_click)
        for w in [self.txt_plaka, self.txt_marka, self.txt_model, self.txt_yil, self.txt_yakit, self.txt_vites, self.txt_fiyat, btn_ekle]:
            form_layout.addWidget(w)
        layout.addLayout(form_layout)

        buton_layout = QHBoxLayout()
        btn_yenile = QPushButton("Listeyi Yenile"); btn_yenile.clicked.connect(self.verileri_guncelle)
        btn_sil = QPushButton("Seçili Aracı Sil"); btn_sil.clicked.connect(self.arac_sil_click)
        buton_layout.addWidget(btn_yenile); buton_layout.addWidget(btn_sil)
        layout.addLayout(buton_layout)

        self.tablo_arac = QTableWidget()
        self.tablo_arac.setColumnCount(9)
        self.tablo_arac.setHorizontalHeaderLabels(["Araç ID", "Plaka", "Marka", "Model", "Yıl", "Yakıt", "Vites", "Fiyat", "Durum"])
        self.tablo_arac.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tablo_arac.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.tablo_arac)

    def araclari_getir(self):
        self.tablo_arac.setRowCount(0)
        araclar = self.bll.arac_listele()
        if araclar:
            for i, a in enumerate(araclar):
                self.tablo_arac.insertRow(i)
                self.tablo_arac.setItem(i, 0, QTableWidgetItem(str(a['arac_id'])))
                self.tablo_arac.setItem(i, 1, QTableWidgetItem(str(a['plaka'])))
                self.tablo_arac.setItem(i, 2, QTableWidgetItem(str(a['marka'])))
                self.tablo_arac.setItem(i, 3, QTableWidgetItem(str(a['model'])))
                self.tablo_arac.setItem(i, 4, QTableWidgetItem(str(a['yil'])))
                self.tablo_arac.setItem(i, 5, QTableWidgetItem(str(a['yakit_turu'])))
                self.tablo_arac.setItem(i, 6, QTableWidgetItem(str(a['vites_turu'])))
                self.tablo_arac.setItem(i, 7, QTableWidgetItem(str(a['gunluk_fiyat'])))
                self.tablo_arac.setItem(i, 8, QTableWidgetItem(str(a['durum'])))

    def arac_ekle_click(self):
        try:
            self.bll.arac_ekle(self.txt_plaka.text(), self.txt_marka.text(), self.txt_model.text(), 
                               self.txt_yil.text(), self.txt_yakit.text(), self.txt_vites.text(), self.txt_fiyat.text())
            self.verileri_guncelle()
            for box in [self.txt_plaka, self.txt_marka, self.txt_model, self.txt_yil, self.txt_yakit, self.txt_vites, self.txt_fiyat]: box.clear()
        except: pass

    def arac_sil_click(self):
        secili = self.tablo_arac.currentRow()
        if secili >= 0:
            self.bll.arac_sil(self.tablo_arac.item(secili, 0).text())
            self.verileri_guncelle()

    # ================= KİRALAMA SEKME =================
    def init_kiralama_arayuz(self):
        layout = QVBoxLayout(self.sekme_kiralama)
        form_layout = QHBoxLayout()
        
        self.cmb_k_musteri = QComboBox()
        self.cmb_k_arac = QComboBox()
        self.cmb_k_arac.currentIndexChanged.connect(self.kiralama_tutar_hesapla)
        
        self.dt_baslangic = QDateEdit(); self.dt_baslangic.setCalendarPopup(True); self.dt_baslangic.setDisplayFormat("dd.MM.yyyy")
        self.dt_baslangic.setDate(QDate.currentDate())
        self.dt_baslangic.dateChanged.connect(self.kiralama_tutar_hesapla)
        
        self.dt_bitis = QDateEdit(); self.dt_bitis.setCalendarPopup(True); self.dt_bitis.setDisplayFormat("dd.MM.yyyy")
        self.dt_bitis.setDate(QDate.currentDate().addDays(1))
        self.dt_bitis.dateChanged.connect(self.kiralama_tutar_hesapla)
        
        self.txt_k_tutar = QLineEdit(); self.txt_k_tutar.setPlaceholderText("Otomatik Hesaplanır")
        self.txt_k_tutar.setReadOnly(True)
        self.txt_k_tutar.setStyleSheet("background-color: #2b2b2b; font-weight: bold; color: #4CAF50;")
        
        btn_ekle = QPushButton("Kiralama Başlat"); btn_ekle.clicked.connect(self.kiralama_ekle_click)
        for w in [self.cmb_k_musteri, self.cmb_k_arac, self.dt_baslangic, self.dt_bitis, self.txt_k_tutar, btn_ekle]:
            form_layout.addWidget(w)
        layout.addLayout(form_layout)

        buton_layout = QHBoxLayout()
        btn_yenile = QPushButton("Listeyi Yenile"); btn_yenile.clicked.connect(self.verileri_guncelle)
        btn_sil = QPushButton("Seçili Kiralamayı İptal Et"); btn_sil.clicked.connect(self.kiralama_sil_click)
        buton_layout.addWidget(btn_yenile); buton_layout.addWidget(btn_sil)
        layout.addLayout(buton_layout)

        self.tablo_kiralama = QTableWidget()
        self.tablo_kiralama.setColumnCount(7)
        self.tablo_kiralama.setHorizontalHeaderLabels(["Kiralama ID", "Müşteri Ad Soyad", "Araç Plaka", "İşlem Tarihi", "Başlangıç", "Bitiş", "Tutar"])
        self.tablo_kiralama.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tablo_kiralama.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.tablo_kiralama)

    def kiralamalari_getir(self):
        self.tablo_kiralama.setRowCount(0)
        kiralamalar = self.bll.kiralama_listele()
        if kiralamalar:
            for i, k in enumerate(kiralamalar):
                self.tablo_kiralama.insertRow(i)
                self.tablo_kiralama.setItem(i, 0, QTableWidgetItem(str(k['kiralama_id'])))
                self.tablo_kiralama.setItem(i, 1, QTableWidgetItem(str(k['Musteri'])))
                self.tablo_kiralama.setItem(i, 2, QTableWidgetItem(str(k['Arac_Plaka'])))
                self.tablo_kiralama.setItem(i, 3, QTableWidgetItem(str(k['kiralama_tarihi'])))
                self.tablo_kiralama.setItem(i, 4, QTableWidgetItem(str(k['baslangic_tarihi'])))
                self.tablo_kiralama.setItem(i, 5, QTableWidgetItem(str(k['bitis_tarihi'])))
                self.tablo_kiralama.setItem(i, 6, QTableWidgetItem(str(k['toplam_tutar'])))

    def kiralama_tutar_hesapla(self):
        arac_verisi = self.cmb_k_arac.currentData()
        if not arac_verisi:
            self.txt_k_tutar.clear()
            return
        arac_id, gunluk_fiyat = arac_verisi
        gun_sayisi = self.dt_baslangic.date().daysTo(self.dt_bitis.date())
        if gun_sayisi < 1: gun_sayisi = 1
        self.txt_k_tutar.setText(str(gun_sayisi * float(gunluk_fiyat)))

    def kiralama_ekle_click(self):
        musteri_id = self.cmb_k_musteri.currentData()
        arac_verisi = self.cmb_k_arac.currentData()
        if not musteri_id or not arac_verisi: return
        try:
            self.bll.kiralama_ekle(musteri_id, arac_verisi[0], self.dt_baslangic.date().toString("yyyy-MM-dd"), self.dt_bitis.date().toString("yyyy-MM-dd"), self.txt_k_tutar.text())
            self.verileri_guncelle() 
            self.dt_baslangic.setDate(QDate.currentDate())
            self.dt_bitis.setDate(QDate.currentDate().addDays(1))
            QMessageBox.information(self, "Başarılı", "Kiralama başlatıldı! Araç durumu otomatik 'Kirada' oldu.")
        except: pass

    def kiralama_sil_click(self):
        secili = self.tablo_kiralama.currentRow()
        if secili >= 0:
            self.bll.kiralama_sil(self.tablo_kiralama.item(secili, 0).text())
            self.verileri_guncelle()

    # ================= ÖDEME SEKME =================
    def init_odeme_arayuz(self):
        layout = QVBoxLayout(self.sekme_odeme)
        form_layout = QHBoxLayout()
        
        # MÜŞTERİ YERİNE ARTIK KİRALAMALAR LİSTELENİYOR
        self.cmb_o_kiralama = QComboBox() 
        self.cmb_o_kiralama.currentIndexChanged.connect(self.odeme_kiralama_secildi)
        
        self.lbl_borc = QLabel("Toplam Borç: 0.0 TL")
        self.lbl_borc.setStyleSheet("font-weight: bold; color: #ff6666; font-size: 14px; padding: 5px;")
        
        # TUTAR KUTUSUNU OKUNABİLİR (KİLİTLİ) YAPIYORUZ - TEK SEFERDE TAM ÖDEME
        self.txt_o_tutar = QLineEdit(); self.txt_o_tutar.setPlaceholderText("Tutar (Otomatik)")
        self.txt_o_tutar.setReadOnly(True)
        self.txt_o_tutar.setStyleSheet("background-color: #2b2b2b; color: #4CAF50;")
        
        self.txt_o_tur = QLineEdit(); self.txt_o_tur.setPlaceholderText("Tür (Nakit/Kredi)")
        self.txt_o_ack = QLineEdit(); self.txt_o_ack.setPlaceholderText("Açıklama")
        
        btn_ekle = QPushButton("Ödeme Al ve Aracı Teslim Et"); btn_ekle.clicked.connect(self.odeme_ekle_click)
        
        for w in [self.cmb_o_kiralama, self.lbl_borc, self.txt_o_tutar, self.txt_o_tur, self.txt_o_ack, btn_ekle]:
            form_layout.addWidget(w)
        layout.addLayout(form_layout)

        buton_layout = QHBoxLayout()
        btn_yenile = QPushButton("Listeyi Yenile"); btn_yenile.clicked.connect(self.verileri_guncelle)
        btn_sil = QPushButton("Seçili Ödemeyi Sil"); btn_sil.clicked.connect(self.odeme_sil_click)
        buton_layout.addWidget(btn_yenile); buton_layout.addWidget(btn_sil)
        layout.addLayout(buton_layout)

        self.tablo_odeme = QTableWidget()
        self.tablo_odeme.setColumnCount(6)
        self.tablo_odeme.setHorizontalHeaderLabels(["Ödeme ID", "Müşteri Ad Soyad", "İşlem Tarihi", "Tutar", "Tür", "Açıklama"])
        self.tablo_odeme.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tablo_odeme.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.tablo_odeme)

    def odemeleri_getir(self):
        self.tablo_odeme.setRowCount(0)
        odemeler = self.bll.odeme_listele()
        if odemeler:
            for i, o in enumerate(odemeler):
                self.tablo_odeme.insertRow(i)
                self.tablo_odeme.setItem(i, 0, QTableWidgetItem(str(o['odeme_id'])))
                self.tablo_odeme.setItem(i, 1, QTableWidgetItem(str(o['Musteri'])))
                self.tablo_odeme.setItem(i, 2, QTableWidgetItem(str(o['odeme_tarihi'])))
                self.tablo_odeme.setItem(i, 3, QTableWidgetItem(str(o['odeme_tutari'])))
                self.tablo_odeme.setItem(i, 4, QTableWidgetItem(str(o['odeme_turu'])))
                self.tablo_odeme.setItem(i, 5, QTableWidgetItem(str(o['aciklama'])))

    def odeme_kiralama_secildi(self):
        secili_veri = self.cmb_o_kiralama.currentData()
        if secili_veri:
            kiralama_id, musteri_id, tutar = secili_veri
            # Tek seferde ödeme olduğu için tutarı direkt kutuya yazıp kilitliyoruz
            self.txt_o_tutar.setText(str(tutar))
            
            # Fonksiyon puanı gitmesin diye veritabanındaki fonksiyonu çağırıp borcu ekranda gösteriyoruz
            kalan_borc = self.bll.musteri_kalan_borc(musteri_id)
            self.lbl_borc.setText(f"Toplam Borç: {kalan_borc} TL")
        else:
            self.txt_o_tutar.clear()
            self.lbl_borc.setText("Toplam Borç: 0.0 TL")

    def odeme_ekle_click(self):
        secili_veri = self.cmb_o_kiralama.currentData()
        if not secili_veri: 
            QMessageBox.warning(self, "Uyarı", "Lütfen ödemesi alınacak kiralamayı seçin!")
            return
            
        kiralama_id, musteri_id, tutar = secili_veri
        tur = self.txt_o_tur.text()
        ack = self.txt_o_ack.text()
        
        try:
            # 1. Ödemeyi kaydediyoruz
            self.bll.odeme_ekle(musteri_id, tutar, tur, ack)
            
            # 2. Ödeme alındığı için Kiralamayı sonlandırıyoruz (Siliyoruz)
            # Biz kiralamayı silince, daha önce eklediğimiz Trigger aracı otomatik "Müsait" yapacak!
            self.bll.kiralama_sil(kiralama_id)
            
            self.verileri_guncelle()
            for box in [self.txt_o_tur, self.txt_o_ack]: box.clear()
            QMessageBox.information(self, "İşlem Tamam", "Ödeme tahsil edildi!\nKiralama sonlandırıldı ve Araç tekrar Müsait duruma geçti.")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"İşlem başarısız. Hata: {e}")

    def odeme_sil_click(self):
        secili = self.tablo_odeme.currentRow()
        if secili >= 0:
            self.bll.odeme_sil(self.tablo_odeme.item(secili, 0).text())
            self.verileri_guncelle()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = RentACarApp()
    pencere.show()
    sys.exit(app.exec())
