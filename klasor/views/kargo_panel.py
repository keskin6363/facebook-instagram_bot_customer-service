from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QAbstractItemView, QHBoxLayout, QLineEdit, \
    QPushButton, QHeaderView
from views.styles import GLOBAL_STYLE


class KargoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(GLOBAL_STYLE)
        kargo_layout = QVBoxLayout(self)
        kargo_layout.addWidget(QLabel("<h2 style='color: #0f172a;'>🚚 Kargo Lojistik & Sevk Operasyonları</h2>"))

        kargo_layout.addWidget(QLabel("<b>📋 Sevk Bekleyen Yeni Siparişler</b>"))
        giden_filtre_layout = QHBoxLayout()
        self.btn_tarih_popup = QPushButton("📅 Tarih: Bugün");
        self.btn_tarih_popup.setStyleSheet("background-color: #0ea5e9;")
        self.txt_filtre_giden_id = QLineEdit();
        self.txt_filtre_giden_id.setPlaceholderText("Sipariş ID Numarası")
        self.btn_giden_filtrele = QPushButton("🔍 Filtrele")
        self.btn_giden_temizle = QPushButton("❌ Temizle");
        self.btn_giden_temizle.setObjectName("CikisButonu")
        giden_filtre_layout.addWidget(self.btn_tarih_popup);
        giden_filtre_layout.addWidget(self.txt_filtre_giden_id);
        giden_filtre_layout.addWidget(self.btn_giden_filtrele);
        giden_filtre_layout.addWidget(self.btn_giden_temizle)
        kargo_layout.addLayout(giden_filtre_layout)

        self.kargo_satis_table = QTableWidget();
        self.kargo_satis_table.setColumnCount(12)
        self.kargo_satis_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers);
        self.kargo_satis_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.kargo_satis_table.setHorizontalHeaderLabels(
            ["Sipariş ID", "Müşteri Adı", "Telefon No", "Fatura Adresi", "Ürün", "Fiyat", "Ödeme", "Tarih", "Durum",
             "Kargo", "Fatura No", "Seri No"])
        self.kargo_satis_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        kargo_layout.addWidget(self.kargo_satis_table)

        kargo_satis_form = QHBoxLayout()
        self.txt_siparis_id = QLineEdit();
        self.txt_siparis_id.setPlaceholderText("Sipariş ID")
        self.btn_kargo_kodu_uret = QPushButton("🎫 Otomatik Kargo Kodu Üret")
        kargo_satis_form.addWidget(self.txt_siparis_id);
        kargo_satis_form.addWidget(self.btn_kargo_kodu_uret)
        kargo_layout.addLayout(kargo_satis_form)

        kargo_layout.addWidget(QLabel("<br><b>📥 Gelen İade Kargoları</b>"))
        iade_filtre_layout = QHBoxLayout()
        self.txt_filtre_iade_kod = QLineEdit();
        self.txt_filtre_iade_kod.setPlaceholderText("İade Kodu")
        self.btn_iade_filtrele = QPushButton("🔍 Filtrele")
        self.btn_iade_temizle = QPushButton("❌ Temizle");
        self.btn_iade_temizle.setObjectName("CikisButonu")
        iade_filtre_layout.addWidget(self.txt_filtre_iade_kod);
        iade_filtre_layout.addWidget(self.btn_iade_filtrele);
        iade_filtre_layout.addWidget(self.btn_iade_temizle)
        kargo_layout.addLayout(iade_filtre_layout)

        self.kargo_table = QTableWidget();
        self.kargo_table.setColumnCount(6)
        self.kargo_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers);
        self.kargo_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.kargo_table.setHorizontalHeaderLabels(
            ["İade ID", "Müşteri ID", "İade Edilen Ürün", "İade Kodu", "Durum", "İade Tarihi"])
        self.kargo_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        kargo_layout.addWidget(self.kargo_table)

        kargo_iade_form = QHBoxLayout()
        self.txt_kargo_id = QLineEdit();
        self.txt_kargo_id.setPlaceholderText("İade ID")
        self.btn_kargo_onayla = QPushButton("✅ İade Kargo Teslim Alındı")
        kargo_iade_form.addWidget(self.txt_kargo_id);
        kargo_iade_form.addWidget(self.btn_kargo_onayla)
        kargo_layout.addLayout(kargo_iade_form)

        self.btn_kargo_yenile = QPushButton("🔄 Lojistik Yenile");
        self.btn_kargo_yenile.setObjectName("YenileButonu")
        kargo_layout.addWidget(self.btn_kargo_yenile)