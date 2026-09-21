from database.db_manager import DBManager


class InventoryModel:
    def __init__(self):
        self.db = DBManager()

    def process_new_product(self, barcode, product_name, price, stock, serial_numbers):
        """İş mantığı: Ürünü kontrol et, ekle/güncelle, ardından serileri bağla"""
        try:
            # 1. Ürün zaten var mı kontrol et
            mevcut_urun = self.db.get_product_by_barcode(barcode)

            if mevcut_urun:
                product_id = mevcut_urun['id']
                self.db.update_inventory_stock(product_id, stock, price)
            else:
                product_id = self.db.insert_inventory_product(barcode, product_name, price, stock)

            # 2. Seri Numarası İşlemleri (Virgülle ayrılmışsa parçala)
            if serial_numbers:
                seri_listesi = [s.strip() for s in serial_numbers.split(',')]

                for seri in seri_listesi:
                    if seri:  # Boşluk girilmişse atla
                        mevcut_seri = self.db.get_serial_number(seri)
                        if not mevcut_seri:
                            self.db.insert_product_serial(seri, product_id)

            return True
        except Exception as e:
            print(f"❌ Envanter Model Hatası: {e}")
            return False

    def get_inventory(self):
        """Arayüzdeki depoyu doldurmak için tüm ürünleri çeker"""
        return self.db.get_all_inventory()

    def update_product(self, product_id, product_name, price, barcode):
        """Ürün düzenleme işlemini DB Manager'a iletir"""
        try:
            self.db.update_inventory_product(product_id, product_name, price, barcode)
            return True
        except Exception as e:
            print(f"Ürün Güncelleme Hatası: {e}")
            return False

    def delete_product(self, product_id):
        """Ürün silme işlemini DB Manager'a iletir"""
        try:
            self.db.delete_inventory_product(product_id)
            return True
        except Exception as e:
            print(f"Ürün Silme Hatası: {e}")
            return False

    def get_serial_numbers(self, product_id):
        """Ürünün detayındaki seri numaralarını getirir"""
        try:
            return self.db.get_serials_by_product_id(product_id)
        except Exception as e:
            print(f"Seri No Çekme Hatası: {e}")
            return []