from dal import DataAccessLayer
import uuid
from datetime import datetime

class BusinessLogicLayer:
    def __init__(self):
        self.dal = DataAccessLayer()

    def musteri_listele(self): return self.dal.execute_procedure('sp_MusteriListele')
    
    def musteri_ekle(self, tc, ad, soyad, tel, ehliyet, adres):
        self.dal.execute_procedure('sp_MusteriEkle', (str(uuid.uuid4()), tc, ad, soyad, tel, ehliyet, adres))

    def musteri_sil(self, musteri_id): self.dal.execute_procedure('sp_MusteriSil', (musteri_id,))

    def arac_listele(self): return self.dal.execute_procedure('sp_AracListele')
        
    def arac_ekle(self, plaka, marka, model, yil, yakit, vites, fiyat):
        self.dal.execute_procedure('sp_AracEkle', (str(uuid.uuid4()), plaka, marka, model, int(yil), yakit, vites, float(fiyat)))

    def arac_sil(self, arac_id): self.dal.execute_procedure('sp_AracSil', (arac_id,))

    def kiralama_listele(self): return self.dal.execute_procedure('sp_KiralamaListele')
        
    def kiralama_ekle(self, musteri_id, arac_id, baslangic, bitis, tutar):
        islem_tarihi = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.dal.execute_procedure('sp_KiralamaEkle', (str(uuid.uuid4()), musteri_id, arac_id, islem_tarihi, baslangic, bitis, float(tutar)))

    def kiralama_sil(self, kiralama_id): self.dal.execute_procedure('sp_KiralamaSil', (kiralama_id,))

    def odeme_listele(self): return self.dal.execute_procedure('sp_OdemeListele')
        
    def odeme_ekle(self, musteri_id, tutar, tur, aciklama):
        islem_tarihi = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.dal.execute_procedure('sp_OdemeEkle', (str(uuid.uuid4()), musteri_id, islem_tarihi, float(tutar), tur, aciklama))

    def odeme_sil(self, odeme_id): self.dal.execute_procedure('sp_OdemeSil', (odeme_id,))

    # YENİ EKLENEN KISIM: Veritabanındaki fn_MusteriKalanBorc fonksiyonunu çalıştırır
    def musteri_kalan_borc(self, musteri_id):
        conn = self.dal.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT fn_MusteriKalanBorc(%s)", (musteri_id,))
            result = cursor.fetchone()
            return result[0] if result and result[0] is not None else 0
        except: return 0
        finally:
            cursor.close()
            conn.close()