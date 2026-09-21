from database.db_manager import DBManager
from werkzeug.security import generate_password_hash, check_password_hash


class AuthModel:
    def __init__(self):
        self.db = DBManager()  # Kendi veritabanı bağlantı sınıfın

    def verify_user(self, email, password):
        # SQL yok, db_manager'dan veriyi istiyoruz
        user = self.db.get_user_by_email(email)

        if user:
            db_password = user['password_hash']

            # Hem düz metin (123456) hem de Hash destekli hibrit kontrol
            if db_password == password:
                return user['role']
            elif check_password_hash(db_password, password):
                return user['role']

        return None

    def change_password(self, email, old_pass, new_pass):
        # SQL yok, db_manager'dan veriyi istiyoruz
        user = self.db.get_user_by_email(email)

        if user:
            db_password = user['password_hash']
            is_valid = (db_password == old_pass) or check_password_hash(db_password, old_pass)

            if is_valid:
                # Şifreyi hashle ve db_manager'a gönder
                hashed_new_pass = generate_password_hash(new_pass)
                self.db.update_user_password(email, hashed_new_pass)
                return True, "Şifreniz güvenli bir şekilde güncellendi!"

        return False, "Eski şifrenizi hatalı girdiniz!"