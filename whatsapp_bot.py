import pandas as pd
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import logging
from twilio.rest import Client

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

# Inisialisasi Twilio Client
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
verified_phone_number = os.getenv("TWILIO_VERIFIED_NUMBER")
if not all([account_sid, auth_token, twilio_whatsapp_number, verified_phone_number]):
    logger.error("TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, atau TWILIO_VERIFIED_NUMBER tidak ditemukan di .env")
    raise ValueError("Kredensial Twilio tidak lengkap di file .env")
if not verified_phone_number.startswith('+'):
    logger.error(f"TWILIO_VERIFIED_NUMBER ({verified_phone_number}) harus dalam format internasional, misalnya +6281234567890")
    raise ValueError("TWILIO_VERIFIED_NUMBER harus dalam format internasional")
client = Client(account_sid, auth_token)

# Membaca file CSV
def read_menu_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Berhasil membaca file CSV: {file_path}, {len(df)} baris ditemukan")
        return df
    except Exception as e:
        logger.error(f"Gagal membaca file CSV: {file_path}, Error: {str(e)}")
        raise

# Mengirim pesan ke nomor WhatsApp menggunakan Twilio
def send_whatsapp_message(verified_phone_number, message, day):
    try:
        # Tunggu 1 menit untuk pengiriman
        send_time = datetime.now() + timedelta(minutes=1)
        time_to_wait = (send_time - datetime.now()).total_seconds()
        if time_to_wait > 0:
            logger.info(f"Menunggu {time_to_wait} detik hingga {send_time} untuk hari {day}, nomor tujuan: whatsapp:{verified_phone_number}")
            time.sleep(time_to_wait)
        
        # Kirim pesan menggunakan Twilio
        message_obj = client.messages.create(
            body=message,
            from_=f"whatsapp:{twilio_whatsapp_number}",
            to=f"whatsapp:{verified_phone_number}"
        )
        logger.info(f"Pesan dikirim untuk hari {day} ke nomor whatsapp:{verified_phone_number} pada {send_time}, SID: {message_obj.sid}, Status: {message_obj.status}")
    except Exception as e:
        logger.error(f"Gagal mengirim pesan untuk hari {day} ke nomor whatsapp:{verified_phone_number}: {str(e)}")
        raise

# main function to run the bot
def run_menu_bot(file_path, verified_phone_number, start_date):
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
            
            send_whatsapp_message(verified_phone_number, message, day)
            logger.info(f"Selesai mengirim pesan untuk hari {day}, menunggu 60 detik sebelum lanjut")
            time.sleep(60)  # Tunggu 1 menit untuk menghindari spam
                
    except Exception as e:
        logger.error(f"Error dalam run_menu_bot: {str(e)}")
        raise

# Contoh penggunaan
if __name__ == "__main__":
    file_path = "dataset_menu_30_hari.csv"
    verified_phone_number = os.getenv("TWILIO_VERIFIED_NUMBER")  # Ambil ID grup dari .env
    start_date = datetime(2025, 7, 4)  # Tanggal mulai
    
    if verified_phone_number is None:
        logger.error("TWILIO_VERIFIED_NUMBER tidak ditemukan di file .env")
        raise ValueError("TWILIO_VERIFIED_NUMBER tidak ditemukan di file .env")
    
    logger.info(f"Memulai bot WhatsApp dengan Twilio, nomor pengirim: {twilio_whatsapp_number}, nomor tujuan: {verified_phone_number}")
    run_menu_bot(file_path, verified_phone_number, start_date)