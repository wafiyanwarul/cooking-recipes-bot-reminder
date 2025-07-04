import pandas as pd
import pywhatkit
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import logging

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()  # Menampilkan log di konsol juga
    ]
)
logger = logging.getLogger(__name__)

# Memuat variabel lingkungan dari .env
load_dotenv()

# Membaca file CSV
def read_menu_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Berhasil membaca file CSV: {file_path}, {len(df)} baris ditemukan")
        return df
    except Exception as e:
        logger.error(f"Gagal membaca file CSV: {file_path}, Error: {str(e)}")
        raise

# Mengirim pesan ke grup WhatsApp
def send_whatsapp_message(group_id, message, day):
    try:
        pywhatkit.sendwhatmsg_to_group(group_id, message, 5, 0, wait_time=30)
        logger.info(f"Pesan dikirim untuk hari {day} ke grup {group_id}")
    except Exception as e:
        logger.error(f"Gagal mengirim pesan untuk hari {day} ke grup {group_id}: {str(e)}")
        raise

# Fungsi utama untuk menjalankan bot
def run_menu_bot(file_path, group_id, start_date):
    try:
        menu_data = read_menu_csv(file_path)
        
        for index, row in menu_data.iterrows():
            day = row['Hari']
            menu = row['Menu']
            bahan = row['Bahan']
            bumbu = row['Bumbu']
            harga = row['Harga']
            tutorial = row['Tutorial']
            
            # Format pesan
            message = f"Hari {day}:\nMenu: {menu}\nBahan: {bahan}\nBumbu: {bumbu}\nHarga: Rp{harga}\nTutorial: {tutorial}"
            
            # Hitung tanggal pengiriman
            send_date = start_date + timedelta(days=index)
            current_date = datetime.now().date()
            
            if send_date.date() >= current_date:
                logger.info(f"Menjadwalkan pengiriman untuk hari {day} pada {send_date}")
                # Tunggu hingga waktu pengiriman (05:00 WIB)
                time_to_wait = (send_date.replace(hour=5, minute=0, second=0) - datetime.now()).total_seconds()
                if time_to_wait > 0:
                    logger.info(f"Menunggu {time_to_wait} detik hingga pukul 05:00 WIB")
                    time.sleep(time_to_wait)
                send_whatsapp_message(group_id, message, day)
                logger.info(f"Selesai mengirim pesan untuk hari {day}, menunggu 60 detik sebelum lanjut")
                time.sleep(60)  # Tunggu 1 menit untuk menghindari spam
            else:
                logger.info(f"Melewati hari {day} karena tanggal {send_date.date()} sudah lewat")
                
    except Exception as e:
        logger.error(f"Error dalam run_menu_bot: {str(e)}")
        raise

# Contoh penggunaan
if __name__ == "__main__":
    file_path = "dataset_menu_30_hari.csv"
    group_id = os.getenv("WHATSAPP_GROUP_ID")  # Ambil ID grup dari .env
    start_date = datetime(2025, 7, 4)  # Tanggal mulai sesuaikan dengan waktu anda saat ini
    
    if group_id is None:
        logger.error("WHATSAPP_GROUP_ID tidak ditemukan di file .env")
        raise ValueError("WHATSAPP_GROUP_ID tidak ditemukan di file .env")
    
    logger.info("Memulai bot WhatsApp")
    run_menu_bot(file_path, group_id, start_date)
    
    # make sure that your whatsapp web is open in your browser and logged in
    # this output will make your contact in whatsapp send a message to the group using your contact manually because the bot is not able to send message automatically 
    # you can use twilio to send message automatically
    logger.info("Bot WhatsApp selesai dijalankan")

