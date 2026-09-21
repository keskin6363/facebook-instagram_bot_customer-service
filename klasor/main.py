import sys
import traceback
import subprocess
import atexit
from PyQt6.QtWidgets import QApplication
from controllers.main_controller import MainController

# Bot sürecini hafızada tutacağımız global değişken
bot_process = None


def start_bot_service():
    """Uygulama açıldığında bot_service.py dosyasını arka planda otomatik başlatır."""
    global bot_process
    try:
        # sys.executable mevcut Python yolunu (venv) otomatik bulur
        bot_process = subprocess.Popen([sys.executable, "services/bot_service.py"])
        print("✅ Bot Servisi (Port 5000) arka planda otomatik olarak başlatıldı!")
    except Exception as e:
        print(f"❌ Bot servisi başlatılamadı: {e}")


def stop_bot_service():
    """Uygulama kapandığında arka plandaki bot sunucusunu da temiz bir şekilde kapatır."""
    global bot_process
    if bot_process:
        bot_process.terminate()
        print("🛑 ERP Kapatıldı. Arka plandaki Bot Servisi durduruldu.")


# Sistem kapandığında stop_bot_service fonksiyonunu çalıştır
atexit.register(stop_bot_service)


# PyQt6 sessiz çökmeleri engellemek için hata yakalayıcı
def temiz_hata_yakalayici(exc_type, exc_value, exc_tb):
    hata_mesaji = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("\n❌ [SİSTEMDE BİR PYTHON HATASI OLUŞTU] ❌\n", hata_mesaji)


sys.excepthook = temiz_hata_yakalayici

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # --- YENİ: UYGULAMA BAŞLARKEN BOTU DA AYAĞA KALDIR ---
    start_bot_service()

    controller = MainController()
    controller.show_login()
    sys.exit(app.exec())