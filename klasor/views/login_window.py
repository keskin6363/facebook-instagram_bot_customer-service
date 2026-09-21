from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from views.styles import GLOBAL_STYLE


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("GirisEkrani")
        self.setWindowTitle("Güvenli Sistem Girişi")
        self.setFixedSize(360, 260)
        self.setStyleSheet(GLOBAL_STYLE)

        layout = QVBoxLayout()
        layout.setSpacing(14)
        layout.setContentsMargins(30, 30, 30, 30)

        baslik = QLabel("Sistem Girişi")
        baslik.setStyleSheet("font-size: 22px; font-weight: bold; color: #0f172a; margin-bottom: 10px;")
        baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.txt_email = QLineEdit();
        self.txt_email.setPlaceholderText("E-posta Adresi")
        self.txt_sifre = QLineEdit();
        self.txt_sifre.setPlaceholderText("Şifre")
        self.txt_sifre.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_giris = QPushButton("Giriş Yap")

        layout.addWidget(baslik);
        layout.addWidget(self.txt_email);
        layout.addWidget(self.txt_sifre);
        layout.addWidget(self.btn_giris)
        self.setLayout(layout)

        self.txt_sifre.returnPressed.connect(self.btn_giris.click)
        self.txt_email.returnPressed.connect(self.btn_giris.click)