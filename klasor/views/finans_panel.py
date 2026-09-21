from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QLineEdit, QPushButton, QTableWidget, \
    QAbstractItemView, QHeaderView
from views.styles import GLOBAL_STYLE


class FinansPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(GLOBAL_STYLE)
        finans_ana_layout = QVBoxLayout(self)
        finans_ana_layout.addWidget(QLabel("<h2 style='color: #0f172a;'>📊 Finans ve Muhasebe Yönetimi</h2>"))

        ozet_widget = QWidget()
        ozet_widget.setStyleSheet(
            "background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px;")
        ozet_layout = QHBoxLayout(ozet_widget)

        col_satis = QVBoxLayout()
        self.lbl_d_satis = QLabel("<b>Günlük Satış:</b> 0.00 TL")
        self.lbl_m_satis = QLabel("<b>Aylık Satış:</b> 0.00 TL")
        self.lbl_d_satis.setStyleSheet("color: #0284c7; font-size: 13px;")
        self.lbl_m_satis.setStyleSheet("color: #0369a1; font-weight: bold; font-size: 14px;")
        col_satis.addWidget(self.lbl_d_satis);
        col_satis.addWidget(self.lbl_m_satis)

        col_iade = QVBoxLayout()
        self.lbl_d_iade = QLabel("<b>Günlük İade:</b> -0.00 TL")
        self.lbl_m_iade = QLabel("<b>Aylık İade:</b> -0.00 TL")
        self.lbl_d_iade.setStyleSheet("color: #ea580c; font-size: 13px;")
        self.lbl_m_iade.setStyleSheet("color: #c2410c; font-weight: bold; font-size: 14px;")
        col_iade.addWidget(self.lbl_d_iade);
        col_iade.addWidget(self.lbl_m_iade)

        col_net = QVBoxLayout()
        self.lbl_d_net = QLabel("<b>GÜNLÜK NET:</b> 0.00 TL")
        self.lbl_m_net = QLabel("<b>AYLIK NET:</b> 0.00 TL")
        self.lbl_d_net.setStyleSheet("color: #16a34a; font-weight: bold; font-size: 13px;")
        self.lbl_m_net.setStyleSheet("color: #15803d; font-weight: bold; font-size: 15px;")
        col_net.addWidget(self.lbl_d_net);
        col_net.addWidget(self.lbl_m_net)

        col_gider = QVBoxLayout()
        self.lbl_d_gider = QLabel("<b>Günlük Gider:</b> 0.00 TL")
        self.lbl_m_gider = QLabel("<b>Aylık Gider:</b> 0.00 TL")
        self.lbl_d_gider.setStyleSheet("color: #ef4444; font-size: 13px;")
        self.lbl_m_gider.setStyleSheet("color: #b91c1c; font-weight: bold; font-size: 14px;")
        col_gider.addWidget(self.lbl_d_gider);
        col_gider.addWidget(self.lbl_m_gider)

        ozet_layout.addLayout(col_satis);
        ozet_layout.addLayout(col_iade);
        ozet_layout.addLayout(col_net);
        ozet_layout.addLayout(col_gider)
        finans_ana_layout.addWidget(ozet_widget)

        self.finans_tabs = QTabWidget()

        self.tab_satislar = QWidget();
        satis_layout = QVBoxLayout(self.tab_satislar)
        filtre_layout = QHBoxLayout()
        self.btn_tarih_popup = QPushButton("📅 Tarih: Bugün");
        self.btn_tarih_popup.setStyleSheet("background-color: #0ea5e9;")
        self.txt_filtre_siparis_id = QLineEdit();
        self.txt_filtre_siparis_id.setPlaceholderText("Sipariş ID")
        self.txt_filtre_fatura_no = QLineEdit();
        self.txt_filtre_fatura_no.setPlaceholderText("Fatura No")
        self.btn_filtre_uygula = QPushButton("🔍 Filtrele")
        self.btn_filtre_temizle = QPushButton("❌ Temizle");
        self.btn_filtre_temizle.setObjectName("CikisButonu")
        filtre_layout.addWidget(self.btn_tarih_popup);
        filtre_layout.addWidget(self.txt_filtre_siparis_id);
        filtre_layout.addWidget(self.txt_filtre_fatura_no);
        filtre_layout.addWidget(self.btn_filtre_uygula);
        filtre_layout.addWidget(self.btn_filtre_temizle)
        satis_layout.addLayout(filtre_layout)

        self.finans_satis_table = QTableWidget()
        self.finans_satis_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers);
        self.finans_satis_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.finans_satis_table.setColumnCount(12)
        self.finans_satis_table.setHorizontalHeaderLabels(
            ["Sipariş ID", "Müşteri", "Telefon No", "Fatura Adresi", "Ürün", "Fiyat", "Ödeme", "Tarih", "Durum",
             "Kargo", "Fatura No", "Seri No"])
        self.finans_satis_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        satis_layout.addWidget(self.finans_satis_table)

        fatura_layout = QHBoxLayout()
        self.txt_fatura_siparis_id = QLineEdit();
        self.txt_fatura_siparis_id.setPlaceholderText("Sipariş ID")
        self.txt_fatura_no_giris = QLineEdit();
        self.txt_fatura_no_giris.setPlaceholderText("Fatura No")
        self.btn_fatura_kaydet = QPushButton("📄 Faturayı İşle")
        fatura_layout.addWidget(self.txt_fatura_siparis_id);
        fatura_layout.addWidget(self.txt_fatura_no_giris);
        fatura_layout.addWidget(self.btn_fatura_kaydet)
        satis_layout.addLayout(fatura_layout)

        self.tab_iadeler = QWidget();
        iade_layout = QVBoxLayout(self.tab_iadeler)
        self.finans_table = QTableWidget();
        self.finans_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers);
        self.finans_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.finans_table.setColumnCount(6)
        self.finans_table.setHorizontalHeaderLabels(
            ["İade ID", "Müşteri ID", "İade Edilen Ürün", "İade Kodu", "Durum", "İade Tarihi"])
        self.finans_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        iade_layout.addWidget(self.finans_table)

        self.tab_masraflar = QWidget();
        masraf_layout = QVBoxLayout(self.tab_masraflar)
        masraf_ekle_layout = QHBoxLayout()
        self.txt_masraf_adi = QLineEdit();
        self.txt_masraf_adi.setPlaceholderText("Gider Açıklaması")
        self.txt_masraf_tutari = QLineEdit();
        self.txt_masraf_tutari.setPlaceholderText("Tutar (TL)")
        self.btn_masraf_ekle = QPushButton("💸 Masraf Ekle")
        masraf_ekle_layout.addWidget(self.txt_masraf_adi);
        masraf_ekle_layout.addWidget(self.txt_masraf_tutari);
        masraf_ekle_layout.addWidget(self.btn_masraf_ekle)
        masraf_layout.addLayout(masraf_ekle_layout)

        self.masraf_table = QTableWidget();
        self.masraf_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers);
        self.masraf_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.masraf_table.setColumnCount(4)
        self.masraf_table.setHorizontalHeaderLabels(["Gider ID", "Açıklama", "Tutar (TL)", "Tarih"])
        self.masraf_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        masraf_layout.addWidget(self.masraf_table)

        self.tab_personel_finans = QWidget();
        personel_finans_layout = QVBoxLayout(self.tab_personel_finans)
        self.finans_personel_table = QTableWidget();
        self.finans_personel_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers);
        self.finans_personel_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.finans_personel_table.setColumnCount(7)
        self.finans_personel_table.setHorizontalHeaderLabels(
            ["Per. ID", "Ad Soyad", "Giriş E-postası", "Sistem Rolü", "Maaş (TL)", "Banka/IBAN", "İşe Giriş"])
        self.finans_personel_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        personel_finans_layout.addWidget(self.finans_personel_table)

        self.finans_tabs.addTab(self.tab_satislar, "🛒 Satışlar/Faturalar");
        self.finans_tabs.addTab(self.tab_iadeler, "🔄 İadeler");
        self.finans_tabs.addTab(self.tab_masraflar, "📉 Genel Masraflar");
        self.finans_tabs.addTab(self.tab_personel_finans, "👥 Personel Giderleri")
        finans_ana_layout.addWidget(self.finans_tabs)

        self.btn_finans_yenile = QPushButton("🔄 Finans Verilerini Yenile");
        self.btn_finans_yenile.setObjectName("YenileButonu")
        finans_ana_layout.addWidget(self.btn_finans_yenile)