import pandas as pd
import pywhatkit
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load variable form the .env
load_dotenv()

# Read CSV files (main dataset)
def read_menu_csv(file_path):
    
    df = pd.read_csv(file_path)
    return df

# Send the message to WhatsApp Group
def send_whatsapp_message(group_id, message):
    pywhatkit.sendwhatmsg_to_group(group_id, message, 5, 0, wait_time=30)

# Main function tu run the bot
def run_menu_bot(file_path, group_id, start_date):
    menu_data = read_menu_csv(file_path)
    
    for index, row in menu_data.iterrows():
        day = row['Hari']
        menu = row['Menu']
        bahan = row['Bahan']
        bumbu = row['Bumbu']
        harga = row['Harga']
        tutorial = row['Tutorial']
        
        # Format the message
        message = f"Hari {day}:\nMenu: {menu}\nBahan: {bahan}\nBumbu: {bumbu}\nHarga: Rp{harga}\nTutorial: {tutorial}"
        
        # Count down to the date when the message should be sent
        send_date = start_date + timedelta(days=index)
        current_date = datetime.now().date()
        
        if send_date.date() >= current_date:
            # wait until time to send (05:00 WIB)
            time_to_wait = (send_date.replace(hour=10, minute=33, second=30) - datetime.now()).total_seconds()
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            send_whatsapp_message(group_id, message)
            time.sleep(60)  # wait 1 minute to avoid spam

# Contoh penggunaan
if __name__ == "__main__":
    file_path = "dataset_menu_30_hari.csv"
    group_id = os.getenv("WHATSAPP_GROUP_ID")  # retrieve whatsapp group ID from .env
    start_date = datetime(2025, 7, 4)  # start date
    
    if group_id is None:
        raise ValueError("WHATSAPP_GROUP_ID tidak ditemukan di file .env")
    
    run_menu_bot(file_path, group_id, start_date)