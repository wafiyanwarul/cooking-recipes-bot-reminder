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
            
            # Hitung waktu pengiriman (3 menit dari sekarang)
            send_time = datetime.now() + timedelta(minutes=3)
            logger.info(f"Menjadwalkan pengiriman untuk hari {day} pada {send_time}")
            # Tunggu hingga waktu pengiriman
            time_to_wait = (send_time - datetime.now()).total_seconds()
            if time_to_wait > 0:
                logger.info(f"Menunggu {time_to_wait} detik hingga {send_time}")
                time.sleep(time_to_wait)
            send_whatsapp_message(group_id, message, day)
                
    except Exception as e:
        logger.error(f"Error dalam run_menu_bot: {str(e)}")
        raise

# Contoh penggunaan
if __name__ == "__main__":
    file_path = "dataset_menu_30_hari.csv"
    group_id = os.getenv("WHATSAPP_GROUP_ID")  # Ambil ID grup dari .env
    start_date = datetime(2025, 7, 4)  # Tanggal mulai
    
    if group_id is None:
        logger.error("WHATSAPP_GROUP_ID tidak ditemukan di file .env")
        raise ValueError("WHATSAPP_GROUP_ID tidak ditemukan di file .env")
    
    logger.info("Memulai bot WhatsApp")
    run_menu_bot(file_path, group_id, start_date)