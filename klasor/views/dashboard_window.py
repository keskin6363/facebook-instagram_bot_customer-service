from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QStackedWidget, QPushButton
from PyQt6.QtCore import Qt
from views.styles import GLOBAL_STYLE
from views.finans_panel import FinansPanel
from views.depo_panel import DepoPanel
from views.kargo_panel import KargoPanel
from views.ik_panel import IkPanel



class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("AnaEkran")
        self.setWindowTitle("Kurumsal Yönetim Sistemi (ERP & WMS)")
        self.setGeometry(100, 100, 1250, 750)
        self.setStyleSheet(GLOBAL_STYLE)
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(15, 15, 15, 15)

        self.sol_panel_widget = QWidget()
        sol_layout = QVBoxLayout()
        sol_layout.setContentsMargins(0, 0, 0, 0)
        sirket_lbl = QLabel("🤖 ERP SYSTEM")
        sirket_lbl.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: bold; padding: 10px;")
        sirket_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sol_menu = QListWidget()
        self.btn_sifre_degistir = QPushButton("🔑 Şifre Değiştir");
        self.btn_sifre_degistir.setObjectName("SifreButonu")
        self.btn_geri = QPushButton("🚪 Güvenli Çıkış");
        self.btn_geri.setObjectName("CikisButonu")

        sol_layout.addWidget(sirket_lbl);
        sol_layout.addWidget(self.sol_menu)
        sol_layout.addWidget(self.btn_sifre_degistir);
        sol_layout.addWidget(self.btn_geri)
        self.sol_panel_widget.setLayout(sol_layout)

        self.icerik_pencereleri = QStackedWidget()
        self.main_layout.addWidget(self.sol_panel_widget, 2)
        self.main_layout.addWidget(self.icerik_pencereleri, 8)
        self.setLayout(self.main_layout)

        # Panel Alt Sınıf Örnekleri (Alt modüllerden yüklenir)
        self.finans_ekrani = FinansPanel()
        self.depo_ekrani = DepoPanel()
        self.kargo_ekrani = KargoPanel()
        self.ik_ekrani = IkPanel()


        self.sol_menu.currentRowChanged.connect(self.icerik_pencereleri.setCurrentIndex)

    def load_role(self, role):
        self.sol_menu.clear()
        while self.icerik_pencereleri.count() > 0:
            self.icerik_pencereleri.removeWidget(self.icerik_pencereleri.widget(0))

        if role == 'yonetici':
            self.sol_menu.addItems(
                ["📊 Finans Paneli", "📦 Depo Yönetimi", "🚚 Kargo Lojistik", "👥 İnsan Kaynakları"])
            self.icerik_pencereleri.addWidget(self.finans_ekrani);
            self.icerik_pencereleri.addWidget(self.depo_ekrani)
            self.icerik_pencereleri.addWidget(self.kargo_ekrani);
            self.icerik_pencereleri.addWidget(self.ik_ekrani);
        elif role == 'ik':
            self.sol_menu.addItem("👥 İnsan Kaynakları");
            self.icerik_pencereleri.addWidget(self.ik_ekrani)
        elif role == 'finans':
            self.sol_menu.addItem("📊 Finans Paneli");
            self.icerik_pencereleri.addWidget(self.finans_ekrani)
        elif role == 'depo':
            self.sol_menu.addItem("📦 Depo Yönetimi");
            self.icerik_pencereleri.addWidget(self.depo_ekrani)
        elif role == 'kargo':
            self.sol_menu.addItem("🚚 Kargo Lojistik");
            self.icerik_pencereleri.addWidget(self.kargo_ekrani)