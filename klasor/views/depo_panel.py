from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QAbstractItemView, QHBoxLayout, QLineEdit, \
    QPushButton, QHeaderView
from PyQt6.QtCore import Qt
from views.styles import GLOBAL_STYLE


class DepoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(GLOBAL_STYLE)
        depo_layout = QVBoxLayout(self)
        depo_layout.addWidget(QLabel("<h2 style='color: #0f172a;'>📦 Depo Envanter & Stok Yönetimi</h2>"))

        depo_filtre_layout = QHBoxLayout()
        self.txt_filtre_barkod = QLineEdit();
        self.txt_filtre_barkod.setPlaceholderText("Barkod Numarası")
        self.txt_filtre_urun = QLineEdit();
        self.txt_filtre_urun.setPlaceholderText("Ürün Adı")
        self.btn_depo_filtrele = QPushButton("🔍 Filtrele")
        self.btn_depo_temizle = QPushButton("❌ Temizle");
        self.btn_depo_temizle.setObjectName("CikisButonu")
        depo_filtre_layout.addWidget(self.txt_filtre_barkod);
        depo_filtre_layout.addWidget(self.txt_filtre_urun)
        depo_filtre_layout.addWidget(self.btn_depo_filtrele);
        depo_filtre_layout.addWidget(self.btn_depo_temizle)
        depo_layout.addLayout(depo_filtre_layout)

        self.depo_table = QTableWidget()
        self.depo_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.depo_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.depo_table.setColumnCount(5)
        self.depo_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.depo_table.setHorizontalHeaderLabels(
            ["Ürün ID", "Barkod", "Ürün Tanımı", "Birim Fiyatı (TL)", "Mevcut Stok Adedi"])
        self.depo_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        depo_layout.addWidget(self.depo_table)

        depo_form = QHBoxLayout()
        self.txt_barkod = QLineEdit();
        self.txt_barkod.setPlaceholderText("Barkod No")
        self.txt_urun = QLineEdit();
        self.txt_urun.setPlaceholderText("Yeni Ürün Adı")
        self.txt_fiyat = QLineEdit();
        self.txt_fiyat.setPlaceholderText("Fiyat (TL)")
        self.txt_seri_nolar = QLineEdit();
        self.txt_seri_nolar.setPlaceholderText("Seri Nolar (Virgülle Ayırın)")
        self.btn_depo_ekle = QPushButton("➕ Stok Kartı Aç")
        depo_form.addWidget(self.txt_barkod);
        depo_form.addWidget(self.txt_urun);
        depo_form.addWidget(self.txt_fiyat);
        depo_form.addWidget(self.txt_seri_nolar);
        depo_form.addWidget(self.btn_depo_ekle)
        depo_layout.addLayout(depo_form)

        self.btn_depo_yenile = QPushButton("🔄 Envanteri Yenile");
        self.btn_depo_yenile.setObjectName("YenileButonu")
        depo_layout.addWidget(self.btn_depo_yenile)