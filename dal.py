import mysql.connector
import os

class DataAccessLayer:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        # Kod buraya bakıyor, eğer bilgisayarda MYSQL_PASS diye bir şey tanımlıysa onu alıyor
        # Değilse varsayılan olarak "" (şifresiz) deniyor.
        self.password = os.getenv("MYSQL_PASS", "") 
        self.database = "abc_rentacar"

   
    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def execute_procedure(self, proc_name, params=None):
        conn = self.connect() # Artık burası hata vermeyecek
        cursor = conn.cursor(dictionary=True)
        try:
            if params:
                cursor.callproc(proc_name, params)
            else:
                cursor.callproc(proc_name)
            
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            
            conn.commit()
            return results
        except Exception as e:
            print(f"Veritabanı Hatası: {e}")
            return None
        finally:
            cursor.close()
            conn.close()