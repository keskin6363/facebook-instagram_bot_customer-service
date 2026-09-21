from database.db_manager import DBManager

class CustomerModel:
    def __init__(self): self.db = DBManager()
    def get_customer(self, facebook_id): return self.db.get_customer(facebook_id)
    def save_or_update_customer(self, facebook_id, full_name, phone, address): self.db.upsert_customer(facebook_id, full_name, phone, address)