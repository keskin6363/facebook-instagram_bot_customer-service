from werkzeug.security import generate_password_hash
from database.db_manager import DBManager # Kendi dosya yoluna göre ayarla

class PersonnelModel:
    def __init__(self):
        self.db = DBManager()

    def add_personnel(self, full_name, email, plain_password, role, salary, bank_iban):
        """Şifreyi hashler ve db_manager'a iletir"""
        try:
            hashed_password = generate_password_hash(plain_password)
            self.db.insert_personnel(full_name, email, hashed_password, role, salary, bank_iban)
            return True
        except Exception as e:
            print(f"Personel Ekleme Hatası: {e}")
            raise e

    def get_all_personnel(self):
        """Arayüzü doldurmak için tüm personeli db_manager'dan çeker"""
        return self.db.get_all_personnel()

    def update_personnel(self, p_id, full_name, email, role, salary, bank_iban):
        """Personel düzenleme işlemini db_manager'a iletir"""
        try:
            self.db.update_personnel(p_id, full_name, email, role, salary, bank_iban)
            return True
        except Exception as e:
            print(f"Personel Güncelleme Hatası: {e}")
            return False

    def delete_personnel(self, p_id):
        """Personel silme işlemini db_manager'a iletir"""
        try:
            self.db.delete_personnel(p_id)
            return True
        except Exception as e:
            print(f"Personel Silme Hatası: {e}")
            return False