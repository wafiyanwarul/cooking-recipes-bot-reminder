# WhatsApp Menu Bot

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Twilio](https://img.shields.io/badge/Twilio-API-red)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

A WhatsApp bot that sends daily menu recipes to a specified WhatsApp number using the Twilio API. The bot reads a 30-day menu dataset from a CSV file and sends formatted messages containing the menu, ingredients, seasonings, price, and cooking instructions.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Dataset](#dataset)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
This project automates the daily sharing of cooking recipes via WhatsApp. It uses a CSV file (`dataset_menu_30_hari.csv`) containing 30 days of menu data, including:
- Day number
- Menu name
- Ingredients (`Bahan`)
- Seasonings (`Bumbu`)
- Price (`Harga`)
- Cooking instructions (`Tutorial`)

The bot sends one menu per day (or in testing mode, every minute) to a specified WhatsApp number using Twilio's WhatsApp API. All activities are logged in `bot.log` for debugging and monitoring.

## Features
- Sends daily menu recipes to a WhatsApp number.
- Supports testing mode (sends messages every minute).
- Logs all actions (CSV reading, message sending, errors) to a file and console.
- Securely stores Twilio credentials using a `.env` file.
- Easy to configure and extend for other datasets or schedules.

## Prerequisites
- **Python 3.8+** installed on your system.
- A **Twilio account** with an active WhatsApp-enabled number (free trial available).
- A **verified WhatsApp number** for receiving messages (required in Twilio trial mode).
- Git installed for cloning the repository.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/whatsapp-menu-bot.git
   cd whatsapp-menu-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install pandas twilio python-dotenv
   ```

3. **Download the Dataset**:
   - The dataset (`dataset_menu_30_hari.csv`) is included in the repository. It contains 30 days of Indonesian menu recipes.

## Configuration
1. **Set Up Twilio Account**:
   - Sign up for a Twilio account at [twilio.com](https://www.twilio.com/try-twilio).
   - Get your **Account SID**, **Auth Token**, and **WhatsApp Number** from the [Twilio Console](https://www.twilio.com/console).
   - Verify your personal WhatsApp number in **Phone Numbers > Manage > Verified Numbers** to receive messages in trial mode.
   - Send a message with the word "join" to your Twilio WhatsApp number (e.g., `+14155238886`) from your verified number to connect to the Twilio Sandbox.

2. **Create `.env` File**:
   - Copy the provided `.env.example` to a new file named `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` with your Twilio credentials and verified WhatsApp number:
     ```plaintext
     TWILIO_VERIFIED_NUMBER=+6281234567890  # Your verified WhatsApp number
     TWILIO_ACCOUNT_SID=your_account_sid
     TWILIO_AUTH_TOKEN=your_auth_token
     TWILIO_WHATSAPP_NUMBER=+14155238886  # Twilio WhatsApp number
     ```

3. **Ensure Dataset**:
   - Verify that `dataset_menu_30_hari.csv` is in the project directory. No changes are needed unless you want to customize the menu data.

## Running the Bot
1. **Test Mode (1-Minute Intervals)**:
   - Run the bot to send messages every minute (for testing):
     ```bash
     python whatsapp_bot.py
     ```
   - The bot will read `dataset_menu_30_hari.csv` and send the first menu to your verified WhatsApp number after ~1 minute, with subsequent messages sent every ~1 minute.
   - Check your WhatsApp for messages from the Twilio number (e.g., `+14155238886`).
   - View logs in `bot.log` for details (e.g., message SID, status).

2. **Production Mode (Daily at 05:00 WIB)**:
   - To switch to daily scheduling at 05:00 WIB, modify `whatsapp_bot.py` as follows:
     - In `send_whatsapp_message`, replace the timing logic:
       ```python
       # Replace this:
       send_time = datetime.now() + timedelta(minutes=1)
       time_to_wait = (send_time - datetime.now()).total_seconds()
       if time_to_wait > 0:
           logger.info(f"Menunggu {time_to_wait} detik hingga {send_time} untuk hari {day}, nomor tujuan: whatsapp:{verified_phone_number}")
           time.sleep(time_to_wait)
       # With this:
       send_date = datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)
       if send_date < datetime.now():
           send_date += timedelta(days=1)
       time_to_wait = (send_date - datetime.now()).total_seconds()
       if time_to_wait > 0:
           logger.info(f"Menunggu {time_to_wait} detik hingga {send_date} untuk hari {day}, nomor tujuan: whatsapp:{verified_phone_number}")
           time.sleep(time_to_wait)
       ```
     - In `run_menu_bot`, replace the loop logic:
       ```python
       # Replace this:
       send_whatsapp_message(verified_phone_number, message, day)
       logger.info(f"Selesai mengirim pesan untuk hari {day}, menunggu 60 detik sebelum lanjut")
       time.sleep(60)
       # With this:
       send_date = start_date + timedelta(days=index)
       current_date = datetime.now().date()
       if send_date.date() >= current_date:
           send_whatsapp_message(verified_phone_number, message, day)
           logger.info(f"Selesai mengirim pesan untuk hari {day}, menunggu hingga hari berikutnya")
           time.sleep(86400)
       else:
           logger.info(f"Melewati hari {day} karena tanggal {send_date.date()} sudah lewat")
       ```
   - Run the bot again:
     ```bash
     python whatsapp_bot.py
     ```

## Dataset
The dataset (`dataset_menu_30_hari.csv`) contains 30 days of Indonesian recipes with the following columns:
- `Hari`: Day number (1-30)
- `Menu`: Name of the dish
- `Bahan`: Ingredients
- `Bumbu`: Seasonings
- `Harga`: Price in IDR
- `Tutorial`: Cooking instructions

You can customize the dataset by editing `dataset_menu_30_hari.csv` or replacing it with your own CSV file, ensuring the column names remain the same.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make changes and commit (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Create a pull request.

Please ensure your code follows Python PEP 8 style guidelines and includes appropriate logging.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
