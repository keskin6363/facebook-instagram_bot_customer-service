from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QAbstractItemView, QHBoxLayout, QLineEdit, \
    QComboBox, QPushButton, QHeaderView
from PyQt6.QtCore import Qt
from views.styles import GLOBAL_STYLE


class IkPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(GLOBAL_STYLE)
        ik_layout = QVBoxLayout(self)
        ik_layout.addWidget(QLabel("<h2 style='color: #0f172a;'>👥 İnsan Kaynakları Yönetimi</h2>"))

        # --- YENİ: İK FİLTRELEME ÇUBUĞU ---
        ik_filtre_layout = QHBoxLayout()
        self.txt_filtre_ad = QLineEdit();
        self.txt_filtre_ad.setPlaceholderText("Personel Adı Soyadı")
        self.txt_filtre_rol = QLineEdit();
        self.txt_filtre_rol.setPlaceholderText("Departman Rolü (Örn: depo)")
        self.btn_ik_filtrele = QPushButton("🔍 Filtrele")
        self.btn_ik_temizle = QPushButton("❌ Temizle");
        self.btn_ik_temizle.setObjectName("CikisButonu")
        ik_filtre_layout.addWidget(self.txt_filtre_ad);
        ik_filtre_layout.addWidget(self.txt_filtre_rol)
        ik_filtre_layout.addWidget(self.btn_ik_filtrele);
        ik_filtre_layout.addWidget(self.btn_ik_temizle)
        ik_layout.addLayout(ik_filtre_layout)

        self.ik_table = QTableWidget()
        self.ik_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ik_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ik_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ik_table.setColumnCount(7)
        self.ik_table.setHorizontalHeaderLabels(
            ["Per. ID", "Ad Soyad", "Giriş E-postası", "Sistem Rolü", "Maaş (TL)", "Banka/IBAN Bilgisi",
             "İşe Giriş Tarihi"])
        self.ik_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        ik_layout.addWidget(self.ik_table)

        ik_form_widget = QWidget()
        ik_form_widget.setStyleSheet(
            "background-color: #f8fafc; border-radius: 8px; padding: 5px; border: 1px solid #e2e8f0;")
        ik_form = QHBoxLayout(ik_form_widget)

        self.txt_ik_ad = QLineEdit();
        self.txt_ik_ad.setPlaceholderText("Personel Adı Soyadı")
        self.txt_ik_email = QLineEdit();
        self.txt_ik_email.setPlaceholderText("E-posta (Giriş ID)")
        self.txt_ik_sifre = QLineEdit();
        self.txt_ik_sifre.setPlaceholderText("Giriş Şifresi");
        self.txt_ik_sifre.setEchoMode(QLineEdit.EchoMode.Password)
        self.cmb_ik_rol = QComboBox();
        self.cmb_ik_rol.addItems(['yonetici', 'ik', 'finans', 'depo', 'kargo'])
        self.txt_ik_maas = QLineEdit();
        self.txt_ik_maas.setPlaceholderText("Maaş (TL)")
        self.txt_ik_banka = QLineEdit();
        self.txt_ik_banka.setPlaceholderText("Banka IBAN")
        self.btn_ik_ekle = QPushButton("➕ İşe Al / Kaydet")

        ik_form.addWidget(self.txt_ik_ad);
        ik_form.addWidget(self.txt_ik_email);
        ik_form.addWidget(self.txt_ik_sifre)
        ik_form.addWidget(self.cmb_ik_rol);
        ik_form.addWidget(self.txt_ik_maas);
        ik_form.addWidget(self.txt_ik_banka);
        ik_form.addWidget(self.btn_ik_ekle)
        ik_layout.addWidget(ik_form_widget)

        self.btn_ik_yenile = QPushButton("🔄 Personel Listesini Yenile");
        self.btn_ik_yenile.setObjectName("YenileButonu")
        ik_layout.addWidget(self.btn_ik_yenile)