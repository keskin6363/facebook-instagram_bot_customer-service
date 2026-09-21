from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QMenu
from models.auth_model import AuthModel
from models.personnel_model import PersonnelModel
from models.inventory_model import InventoryModel
from models.finance_model import FinanceModel
from models.return_model import ReturnModel
from models.bot_model import BotModel
from views.login_window import LoginWindow
from views.dashboard_window import DashboardWindow
from views.dialogs import SifreDegistirDialog, SeriNumaralariDialog, UrunDuzenleDialog, PersonelDuzenleDialog, \
    TakvimDialog


class MainController:
    def __init__(self):
        self.auth_model = AuthModel()
        self.personnel_model = PersonnelModel()
        self.inventory_model = InventoryModel()
        self.finance_model = FinanceModel()
        self.return_model = ReturnModel()
        self.bot_model = BotModel()

        self.login_view = LoginWindow()
        self.dashboard_view = DashboardWindow()
        self.current_user_email = None

        self.all_orders_data = []
        self.all_inventory_data = []
        self.all_personnel_data = []
        self.all_returns_data = []
        self.all_expenses_data = []

        self.current_finans_date = QDate.currentDate()
        self.current_kargo_date = QDate.currentDate()

        self.bind_signals()

    def bind_signals(self):
        self.login_view.btn_giris.clicked.connect(self.handle_login)
        self.dashboard_view.btn_geri.clicked.connect(self.handle_logout)
        self.dashboard_view.btn_sifre_degistir.clicked.connect(self.handle_password_change)

        self.dashboard_view.finans_ekrani.btn_finans_yenile.clicked.connect(self.load_all_data)
        self.dashboard_view.depo_ekrani.btn_depo_yenile.clicked.connect(self.load_inventory_data)
        self.dashboard_view.kargo_ekrani.btn_kargo_yenile.clicked.connect(self.load_all_data)
        self.dashboard_view.ik_ekrani.btn_ik_yenile.clicked.connect(self.load_personnel_data)

        self.dashboard_view.ik_ekrani.btn_ik_ekle.clicked.connect(self.handle_add_personnel)
        self.dashboard_view.depo_ekrani.btn_depo_ekle.clicked.connect(self.handle_add_inventory)
        self.dashboard_view.kargo_ekrani.btn_kargo_kodu_uret.clicked.connect(self.handle_kargo_gonder)
        self.dashboard_view.kargo_ekrani.btn_kargo_onayla.clicked.connect(self.handle_kargo_iade_alindi)
        self.dashboard_view.finans_ekrani.btn_fatura_kaydet.clicked.connect(self.handle_save_invoice)
        self.dashboard_view.finans_ekrani.btn_masraf_ekle.clicked.connect(self.handle_add_expense)

        self.dashboard_view.finans_ekrani.btn_tarih_popup.clicked.connect(self.open_finans_calendar_popup)
        self.dashboard_view.kargo_ekrani.btn_tarih_popup.clicked.connect(self.open_kargo_calendar_popup)

        self.dashboard_view.finans_ekrani.btn_filtre_uygula.clicked.connect(self.handle_finance_filter)
        self.dashboard_view.finans_ekrani.btn_filtre_temizle.clicked.connect(self.handle_finance_filter_clear)
        self.dashboard_view.depo_ekrani.btn_depo_filtrele.clicked.connect(self.handle_depo_filter)
        self.dashboard_view.depo_ekrani.btn_depo_temizle.clicked.connect(self.handle_depo_filter_clear)
        self.dashboard_view.ik_ekrani.btn_ik_filtrele.clicked.connect(self.handle_ik_filter)
        self.dashboard_view.ik_ekrani.btn_ik_temizle.clicked.connect(self.handle_ik_filter_clear)
        self.dashboard_view.kargo_ekrani.btn_giden_filtrele.clicked.connect(self.handle_kargo_giden_filter)
        self.dashboard_view.kargo_ekrani.btn_giden_temizle.clicked.connect(self.handle_kargo_giden_filter_clear)
        self.dashboard_view.kargo_ekrani.btn_iade_filtrele.clicked.connect(self.handle_kargo_iade_filter)
        self.dashboard_view.kargo_ekrani.btn_iade_temizle.clicked.connect(self.handle_kargo_iade_filter_clear)

        # BARKOD OKUYUCU TETİKLERİ
        self.dashboard_view.depo_ekrani.txt_filtre_barkod.returnPressed.connect(self.handle_depo_filter)
        self.dashboard_view.kargo_ekrani.txt_siparis_id.returnPressed.connect(self.handle_kargo_gonder)
        self.dashboard_view.kargo_ekrani.txt_kargo_id.returnPressed.connect(self.handle_kargo_iade_alindi)
        self.dashboard_view.kargo_ekrani.txt_filtre_iade_kod.returnPressed.connect(self.handle_kargo_iade_filter)
        self.dashboard_view.finans_ekrani.txt_filtre_siparis_id.returnPressed.connect(self.handle_finance_filter)
        self.dashboard_view.finans_ekrani.txt_filtre_fatura_no.returnPressed.connect(self.handle_finance_filter)

        self.dashboard_view.ik_ekrani.ik_table.customContextMenuRequested.connect(self.handle_ik_right_click)
        self.dashboard_view.depo_ekrani.depo_table.customContextMenuRequested.connect(self.handle_depo_right_click)

    def show_login(self):
        self.login_view.show()

    def handle_login(self):
        email = self.login_view.txt_email.text()
        password = self.login_view.txt_sifre.text()
        role = self.auth_model.verify_user(email, password)
        if role:
            self.current_user_email = email
            self.dashboard_view.load_role(role)
            self.login_view.close()
            self.dashboard_view.show()
            self.load_all_data()
        else:
            QMessageBox.warning(self.login_view, "Hata", "Geçersiz giriş bilgileri!")

    def handle_logout(self):
        self.current_user_email = None
        self.dashboard_view.close()
        self.login_view.txt_sifre.clear()
        self.login_view.show()

    def handle_password_change(self):
        dialog = SifreDegistirDialog(self.dashboard_view)
        if dialog.exec():
            success, msg = self.auth_model.change_password(self.current_user_email, dialog.txt_eski.text(),
                                                           dialog.txt_yeni.text())
            QMessageBox.information(self.dashboard_view, "Sonuç", msg) if success else QMessageBox.warning(
                self.dashboard_view, "Hata", msg)

    def open_finans_calendar_popup(self):
        dialog = TakvimDialog(self.dashboard_view, self.current_finans_date)
        if dialog.exec():
            self.current_finans_date = dialog.calendar.selectedDate()
            self.dashboard_view.finans_ekrani.btn_tarih_popup.setText(
                f"📅 Tarih: {self.current_finans_date.toString('dd.MM.yyyy')}")
            self.handle_finance_filter()
            self.filter_expenses_by_calendar()
            self.filter_finans_returns_by_calendar()

    def open_kargo_calendar_popup(self):
        dialog = TakvimDialog(self.dashboard_view, self.current_kargo_date)
        if dialog.exec():
            self.current_kargo_date = dialog.calendar.selectedDate()
            self.dashboard_view.kargo_ekrani.btn_tarih_popup.setText(
                f"📅 Tarih: {self.current_kargo_date.toString('dd.MM.yyyy')}")
            self.handle_kargo_giden_filter()
            self.handle_kargo_iade_filter()

    def load_all_data(self):
        self.load_orders_data()
        self.load_returns_data()
        self.load_inventory_data()
        self.load_expenses_data()
        self.load_personnel_data()

    def load_orders_data(self):
        self.all_orders_data = self.finance_model.get_orders()
        self.handle_finance_filter()
        self.handle_kargo_giden_filter()
        summary = self.finance_model.get_financial_summary()
        if summary:
            self.dashboard_view.finans_ekrani.lbl_d_satis.setText(f"<b>Günlük Satış:</b> {summary['d_sales']:.2f} TL")
            self.dashboard_view.finans_ekrani.lbl_m_satis.setText(f"<b>Aylık Satış:</b> {summary['m_sales']:.2f} TL")
            self.dashboard_view.finans_ekrani.lbl_d_iade.setText(f"<b>Günlük İade:</b> -{summary['d_returns']:.2f} TL")
            self.dashboard_view.finans_ekrani.lbl_m_iade.setText(
                f"<b>Aylık İadeler:</b> -{summary['m_returns']:.2f} TL")
            self.dashboard_view.finans_ekrani.lbl_d_net.setText(f"<b>GÜNLÜK NET:</b> {summary['d_net']:.2f} TL")
            self.dashboard_view.finans_ekrani.lbl_m_net.setText(f"<b>AYLIK NET:</b> {summary['m_net']:.2f} TL")
            self.dashboard_view.finans_ekrani.lbl_d_gider.setText(f"<b>Günlük Gider:</b> {summary['d_exp']:.2f} TL")
            self.dashboard_view.finans_ekrani.lbl_m_gider.setText(f"<b>Aylık Gider:</b> {summary['m_exp']:.2f} TL")

    def load_returns_data(self):
        self.all_returns_data = self.return_model.get_returns()
        self.filter_finans_returns_by_calendar()
        self.handle_kargo_iade_filter()

    def load_inventory_data(self):
        self.all_inventory_data = self.inventory_model.get_inventory()
        self._populate_table(self.dashboard_view.depo_ekrani.depo_table, self.all_inventory_data)

    def load_expenses_data(self):
        self.all_expenses_data = self.finance_model.get_expenses()
        self.filter_expenses_by_calendar()

    def load_personnel_data(self):
        data = self.personnel_model.get_all_personnel()
        self._populate_table(self.dashboard_view.ik_ekrani.ik_table, data)
        self._populate_table(self.dashboard_view.finans_ekrani.finans_personel_table, data)

    def _populate_table(self, table_widget, data):
        table_widget.setRowCount(0)
        for row_index, row_data in enumerate(data):
            table_widget.insertRow(row_index)
            veri_listesi = list(row_data.values())[:table_widget.columnCount()]
            for col_index, value in enumerate(veri_listesi):
                table_widget.setItem(row_index, col_index, QTableWidgetItem("" if value is None else str(value)))

    def handle_finance_filter(self):
        tarih = self.current_finans_date.toString("dd.MM.yyyy")
        f_id = self.dashboard_view.finans_ekrani.txt_filtre_siparis_id.text().strip()
        f_fatura = self.dashboard_view.finans_ekrani.txt_filtre_fatura_no.text().strip().lower()
        res = [o for o in self.all_orders_data if
               str(o.get('date', '')).startswith(tarih) and (not f_id or str(o.get('id')) == f_id) and (
                           not f_fatura or f_fatura in str(o.get('invoice_no', '')).lower())]
        self._populate_table(self.dashboard_view.finans_ekrani.finans_satis_table, res)

    def filter_expenses_by_calendar(self):
        res = [e for e in self.all_expenses_data if
               str(e.get('date', '')).startswith(self.current_finans_date.toString("dd.MM.yyyy"))]
        self._populate_table(self.dashboard_view.finans_ekrani.masraf_table, res)

    def filter_finans_returns_by_calendar(self):
        res = [r for r in self.all_returns_data if
               str(r.get('date', '')).startswith(self.current_finans_date.toString("dd.MM.yyyy"))]
        self._populate_table(self.dashboard_view.finans_ekrani.finans_table, res)

    def handle_finance_filter_clear(self):
        self.dashboard_view.finans_ekrani.txt_filtre_siparis_id.clear()
        self.dashboard_view.finans_ekrani.txt_filtre_fatura_no.clear()
        self.handle_finance_filter()

    def handle_kargo_giden_filter(self):
        tarih = self.current_kargo_date.toString("dd.MM.yyyy")
        f_id = self.dashboard_view.kargo_ekrani.txt_filtre_giden_id.text().strip()
        res = [o for o in self.all_orders_data if
               str(o.get('date', '')).startswith(tarih) and (not f_id or str(o.get('id')) == f_id)]
        self._populate_table(self.dashboard_view.kargo_ekrani.kargo_satis_table, res)

    def handle_kargo_giden_filter_clear(self):
        self.dashboard_view.kargo_ekrani.txt_filtre_giden_id.clear()
        self.handle_kargo_giden_filter()

    def handle_kargo_iade_filter(self):
        tarih = self.current_kargo_date.toString("dd.MM.yyyy")
        f_kod = self.dashboard_view.kargo_ekrani.txt_filtre_iade_kod.text().strip().lower()
        res = [r for r in self.all_returns_data if str(r.get('date', '')).startswith(tarih) and (
                    not f_kod or f_kod in str(r.get('return_code', '')).lower())]
        self._populate_table(self.dashboard_view.kargo_ekrani.kargo_table, res)

    def handle_kargo_iade_filter_clear(self):
        self.dashboard_view.kargo_ekrani.txt_filtre_iade_kod.clear()
        self.handle_kargo_iade_filter()

    def handle_depo_filter(self):
        f_barkod = self.dashboard_view.depo_ekrani.txt_filtre_barkod.text().strip().lower()
        f_urun = self.dashboard_view.depo_ekrani.txt_filtre_urun.text().strip().lower()
        res = [i for i in self.all_inventory_data if
               (not f_barkod or f_barkod in str(i.get('barcode', '')).lower()) and (
                           not f_urun or f_urun in str(i.get('product_name', '')).lower())]
        self._populate_table(self.dashboard_view.depo_ekrani.depo_table, res)

    def handle_depo_filter_clear(self):
        self.dashboard_view.depo_ekrani.txt_filtre_barkod.clear()
        self.dashboard_view.depo_ekrani.txt_filtre_urun.clear()
        self._populate_table(self.dashboard_view.depo_ekrani.depo_table, self.all_inventory_data)

    def handle_ik_filter(self):
        f_ad = self.dashboard_view.ik_ekrani.txt_filtre_ad.text().strip().lower()
        res = [p for p in self.all_personnel_data if (not f_ad or f_ad in str(p.get('full_name', '')).lower())]
        self._populate_table(self.dashboard_view.ik_ekrani.ik_table, res)

    def handle_ik_filter_clear(self):
        self.dashboard_view.ik_ekrani.txt_filtre_ad.clear()
        self._populate_table(self.dashboard_view.ik_ekrani.ik_table, self.all_personnel_data)

    def handle_add_personnel(self):
        ad = self.dashboard_view.ik_ekrani.txt_ik_ad.text().strip()
        email = self.dashboard_view.ik_ekrani.txt_ik_email.text().strip()
        sifre = self.dashboard_view.ik_ekrani.txt_ik_sifre.text().strip()
        rol = self.dashboard_view.ik_ekrani.cmb_ik_rol.currentText()
        maas = self.dashboard_view.ik_ekrani.txt_ik_maas.text().strip().replace(',', '.')
        banka = self.dashboard_view.ik_ekrani.txt_ik_banka.text().strip()
        if ad and email and sifre and maas.replace('.', '', 1).isdigit() and banka:
            try:
                self.personnel_model.add_personnel(ad, email, sifre, rol, float(maas), banka)
                self.load_personnel_data()
                self.dashboard_view.ik_ekrani.txt_ik_ad.clear()
                self.dashboard_view.ik_ekrani.txt_ik_email.clear()
                self.dashboard_view.ik_ekrani.txt_ik_sifre.clear()
                self.dashboard_view.ik_ekrani.txt_ik_maas.clear()
                self.dashboard_view.ik_ekrani.txt_ik_banka.clear()
                QMessageBox.information(self.dashboard_view, "Başarılı", "Personel eklendi.")
            except Exception:
                QMessageBox.critical(self.dashboard_view, "Hata", "E-posta kayıtlı!")

    def handle_ik_right_click(self, position):
        row = self.dashboard_view.ik_ekrani.ik_table.rowAt(position.y())
        if row < 0: return
        menu = QMenu()
        duzenle_action = menu.addAction("✏️ Personeli Düzenle")
        sil_action = menu.addAction("❌ Sistemden Sil")
        action = menu.exec(self.dashboard_view.ik_ekrani.ik_table.viewport().mapToGlobal(position))
        p_id = self.dashboard_view.ik_ekrani.ik_table.item(row, 0).text()
        if action == duzenle_action:
            current_data = {'ad': self.dashboard_view.ik_ekrani.ik_table.item(row, 1).text(),
                            'email': self.dashboard_view.ik_ekrani.ik_table.item(row, 2).text(),
                            'rol': self.dashboard_view.ik_ekrani.ik_table.item(row, 3).text(),
                            'maas': self.dashboard_view.ik_ekrani.ik_table.item(row, 4).text(),
                            'banka': self.dashboard_view.ik_ekrani.ik_table.item(row, 5).text()}
            dialog = PersonelDuzenleDialog(self.dashboard_view, current_data)
            if dialog.exec():
                self.personnel_model.update_personnel(p_id, dialog.txt_ad.text(), dialog.txt_email.text(),
                                                      dialog.cmb_rol.currentText(),
                                                      dialog.txt_maas.text().replace(',', '.'), dialog.txt_banka.text())
                self.load_personnel_data()
        elif action == sil_action:
            if QMessageBox.question(self.dashboard_view, "Onay", "Silinsin mi?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                self.personnel_model.delete_personnel(p_id)
                self.load_personnel_data()

    # ============================================================
    # 📦 ENVANTER EKLEME FONKSİYONU (MVC'ye Göre Güncellendi)
    # ============================================================
    def handle_add_inventory(self):
        barkod = self.dashboard_view.depo_ekrani.txt_barkod.text().strip() or "BARKOD-YOK"
        urun = self.dashboard_view.depo_ekrani.txt_urun.text().strip()
        fiyat = self.dashboard_view.depo_ekrani.txt_fiyat.text().strip().replace(',', '.')
        seri_text = self.dashboard_view.depo_ekrani.txt_seri_nolar.text().strip()

        if urun and seri_text and fiyat.replace('.', '', 1).isdigit():
            # Stok sayısını girilen seri numarası adedine göre otomatik hesaplıyoruz
            seri_listesi = [s.strip() for s in seri_text.split(',') if s.strip()]
            if not seri_listesi:
                QMessageBox.warning(self.dashboard_view, "Uyarı", "Geçerli bir seri numarası girin.")
                return

            stok_miktari = len(seri_listesi)

            # MVC uyumlu yeni model fonksiyonumuzu çağırıyoruz
            basarili_mi = self.inventory_model.process_new_product(barkod, urun, float(fiyat), stok_miktari, seri_text)

            if basarili_mi:
                QMessageBox.information(self.dashboard_view, "Başarılı",
                                        f"✅ {urun} envantere eklendi!\nEklenen Stok Miktarı: {stok_miktari}")
                self.load_inventory_data()
                self.dashboard_view.depo_ekrani.txt_barkod.clear()
                self.dashboard_view.depo_ekrani.txt_urun.clear()
                self.dashboard_view.depo_ekrani.txt_fiyat.clear()
                self.dashboard_view.depo_ekrani.txt_seri_nolar.clear()
            else:
                QMessageBox.critical(self.dashboard_view, "Hata",
                                     "Veritabanına kaydedilirken sorun oluştu. Barkod çakışmasını kontrol edin.")
        else:
            QMessageBox.warning(self.dashboard_view, "Eksik Bilgi",
                                "Lütfen Ürün Adı, Fiyat ve Seri No alanlarını eksiksiz girin.")

    def handle_depo_right_click(self, position):
        row = self.dashboard_view.depo_ekrani.depo_table.rowAt(position.y())
        if row < 0: return
        menu = QMenu()
        duzenle_action = menu.addAction("✏️ Ürünü Düzenle")
        seri_no_action = menu.addAction("🔍 Seri Numaraları")
        sil_action = menu.addAction("❌ Ürünü Sil")
        action = menu.exec(self.dashboard_view.depo_ekrani.depo_table.viewport().mapToGlobal(position))
        product_id = self.dashboard_view.depo_ekrani.depo_table.item(row, 0).text()
        product_name = self.dashboard_view.depo_ekrani.depo_table.item(row, 2).text()
        if action == duzenle_action:
            current_data = {'barkod': self.dashboard_view.depo_ekrani.depo_table.item(row, 1).text(),
                            'ad': product_name, 'fiyat': self.dashboard_view.depo_ekrani.depo_table.item(row, 3).text()}
            dialog = UrunDuzenleDialog(self.dashboard_view, current_data)
            if dialog.exec():
                self.inventory_model.update_product(product_id, dialog.txt_ad.text(),
                                                    dialog.txt_fiyat.text().replace(',', '.'), dialog.txt_barkod.text())
                self.load_inventory_data()
        elif action == seri_no_action:
            dialog = SeriNumaralariDialog(self.dashboard_view, product_name,
                                          self.inventory_model.get_serial_numbers(product_id))
            dialog.exec()
        elif action == sil_action:
            if QMessageBox.question(self.dashboard_view, "Onay", "Silinsin mi?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                self.inventory_model.delete_product(product_id)
                self.load_inventory_data()

    def handle_add_expense(self):
        aciklama = self.dashboard_view.finans_ekrani.txt_masraf_adi.text().strip()
        tutar = self.dashboard_view.finans_ekrani.txt_masraf_tutari.text().strip().replace(',', '.')
        if aciklama and tutar.replace('.', '', 1).isdigit():
            self.finance_model.add_expense(aciklama, float(tutar))
            self.load_expenses_data()
            self.load_orders_data()
            self.dashboard_view.finans_ekrani.txt_masraf_adi.clear()
            self.dashboard_view.finans_ekrani.txt_masraf_tutari.clear()

    def handle_save_invoice(self):
        order_id = self.dashboard_view.finans_ekrani.txt_fatura_siparis_id.text().strip()
        invoice_no = self.dashboard_view.finans_ekrani.txt_fatura_no_giris.text().strip()
        if order_id.isdigit() and invoice_no:
            self.finance_model.update_invoice_number(order_id, invoice_no)
            self.load_orders_data()
            self.dashboard_view.finans_ekrani.txt_fatura_siparis_id.clear()
            self.dashboard_view.finans_ekrani.txt_fatura_no_giris.clear()

    def handle_kargo_gonder(self):
        siparis_id = self.dashboard_view.kargo_ekrani.txt_siparis_id.text()
        if siparis_id.isdigit():
            self.finance_model.assign_tracking_code(siparis_id, "TR-BEKLENIYOR")
            self.load_orders_data()
            self.dashboard_view.kargo_ekrani.txt_siparis_id.clear()

    def handle_kargo_iade_alindi(self):
        row_id = self.dashboard_view.kargo_ekrani.txt_kargo_id.text()
        if row_id.isdigit():
            self.return_model.update_return_status(row_id, "Kargo Alındı / Depoya Yolda")
            self.load_returns_data()
            self.dashboard_view.kargo_ekrani.txt_kargo_id.clear()