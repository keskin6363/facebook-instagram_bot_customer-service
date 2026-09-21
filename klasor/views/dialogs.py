from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox, QVBoxLayout, QLabel, QListWidget, QCalendarWidget, QPushButton
from views.styles import GLOBAL_STYLE

class TakvimDialog(QDialog):
    def __init__(self, parent=None, current_date=None):
        super().__init__(parent); self.setWindowTitle("Tarihi Seçin"); self.setFixedSize(320, 260); self.setStyleSheet(GLOBAL_STYLE)
        layout = QVBoxLayout(self)
        self.calendar = QCalendarWidget(); self.calendar.setGridVisible(True)
        if current_date: self.calendar.setSelectedDate(current_date)
        self.btn_sec = QPushButton("🎯 Tarihi Seç ve Uygula")
        self.btn_sec.clicked.connect(self.accept)
        layout.addWidget(self.calendar); layout.addWidget(self.btn_sec); self.setLayout(layout)

class PersonelDuzenleDialog(QDialog):
    def __init__(self, parent=None, current_data=None):
        if current_data is None: current_data = {}
        super().__init__(parent); self.setWindowTitle("Personel Düzenleme"); self.setFixedSize(380, 280); self.setStyleSheet(GLOBAL_STYLE)
        layout = QFormLayout(); layout.setContentsMargins(20, 20, 20, 20)
        self.txt_ad = QLineEdit(current_data.get('ad', '')); self.txt_email = QLineEdit(current_data.get('email', ''))
        self.cmb_rol = QComboBox(); self.cmb_rol.addItems(['yonetici', 'ik', 'finans', 'depo', 'kargo']); self.cmb_rol.setCurrentText(current_data.get('rol', 'depo'))
        self.txt_maas = QLineEdit(current_data.get('maas', '')); self.txt_banka = QLineEdit(current_data.get('banka', ''))
        layout.addRow("Ad Soyad:", self.txt_ad); layout.addRow("E-posta:", self.txt_email); layout.addRow("Rol:", self.cmb_rol); layout.addRow("Maaş:", self.txt_maas); layout.addRow("IBAN:", self.txt_banka)
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel); self.btns.accepted.connect(self.accept); self.btns.rejected.connect(self.reject)
        layout.addWidget(self.btns); self.setLayout(layout)

class SeriNumaralariDialog(QDialog):
    def __init__(self, parent=None, product_name="", serials=None):
        if serials is None: serials = []
        super().__init__(parent); self.setWindowTitle("Seri No Takip"); self.setFixedSize(450, 350); self.setStyleSheet(GLOBAL_STYLE)
        layout = QVBoxLayout(); self.liste = QListWidget()
        for s in serials: self.liste.addItem(f"🔢 {s['serial_no']} - ({s['status']})")
        layout.addWidget(self.liste); self.setLayout(layout)

class UrunDuzenleDialog(QDialog):
    def __init__(self, parent=None, current_data=None):
        if current_data is None: current_data = {}
        super().__init__(parent); self.setWindowTitle("Ürün Düzenleme"); self.setFixedSize(340, 220); self.setStyleSheet(GLOBAL_STYLE)
        layout = QFormLayout()
        self.txt_ad = QLineEdit(current_data.get('ad', '')); self.txt_barkod = QLineEdit(current_data.get('barkod', '')); self.txt_fiyat = QLineEdit(current_data.get('fiyat', ''))
        layout.addRow("Ürün Adı:", self.txt_ad); layout.addRow("Barkod:", self.txt_barkod); layout.addRow("Fiyat:", self.txt_fiyat)
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel); self.btns.accepted.connect(self.accept); self.btns.rejected.connect(self.reject)
        layout.addWidget(self.btns); self.setLayout(layout)

class SifreDegistirDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Güvenlik Ayarları"); self.setFixedSize(340, 180); self.setStyleSheet(GLOBAL_STYLE)
        layout = QFormLayout()
        self.txt_eski = QLineEdit(); self.txt_eski.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_yeni = QLineEdit(); self.txt_yeni.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Mevcut Şifre:", self.txt_eski); layout.addRow("Yeni Şifre:", self.txt_yeni)
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel); self.btns.accepted.connect(self.accept); self.btns.rejected.connect(self.reject)
        layout.addWidget(self.btns); self.setLayout(layout)