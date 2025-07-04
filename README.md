# WhatsApp Menu Bot (PyWhatKit)

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![PyWhatKit](https://img.shields.io/badge/PyWhatKit-WhatsApp-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

A WhatsApp bot that sends daily menu recipes to a specified WhatsApp group at 05:00 WIB (Western Indonesia Time) using the PyWhatKit library. The bot reads a 30-day menu dataset from a CSV file and sends formatted messages containing the menu, ingredients, seasonings, price, and cooking instructions.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Dataset](#dataset)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
This project automates the daily sharing of cooking recipes to a WhatsApp group. It uses a CSV file (`dataset_menu_30_hari.csv`) containing 30 days of menu data, including:
- Day number (`Hari`)
- Menu name (`Menu`)
- Ingredients (`Bahan`)
- Seasonings (`Bumbu`)
- Price (`Harga`)
- Cooking instructions (`Tutorial`)

The bot sends one menu per day at 05:00 WIB to a specified WhatsApp group using PyWhatKit, which automates WhatsApp Web. All activities are logged in `bot.log` for debugging and monitoring.

**Note**: This bot uses your personal WhatsApp account via WhatsApp Web, so messages will appear as sent from your number.

## Features
- Sends daily menu recipes to a WhatsApp group at 05:00 WIB.
- Reads menu data from a CSV file.
- Logs all actions (CSV reading, message sending, errors) to a file (`bot.log`) and console.
- Securely stores the WhatsApp group ID using a `.env` file.
- Easy to configure and extend for other datasets or schedules.

## Prerequisites
- **Python 3.8+** installed on your system.
- A **WhatsApp account** with access to WhatsApp Web.
- A **WhatsApp group** where you are an admin (to obtain the group ID).
- A web browser (e.g., Chrome, Firefox) for WhatsApp Web automation.
- Git installed for cloning the repository.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/whatsapp-menu-bot.git
   cd whatsapp-menu-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install pandas pywhatkit python-dotenv
   ```

3. **Download the Dataset**:
   - The dataset (`dataset_menu_30_hari.csv`) is included in the repository. It contains 30 days of Indonesian menu recipes.

## Configuration
1. **Get WhatsApp Group ID**:
   - Open WhatsApp Web in your browser and log in with your WhatsApp account.
   - Open the group where you want to send messages.
   - Copy the group invite link (e.g., `https://chat.whatsapp.com/KUUCaTagxvw1ggpDpBkIeo`).
   - The group ID is the part after `https://chat.whatsapp.com/` (e.g., `KUUCaTagxvw1ggpDpBkIeo`).

2. **Create `.env` File**:
   - Copy the provided `.env.example` to a new file named `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` with your WhatsApp group ID:
     ```plaintext
     WHATSAPP_GROUP_ID=your_group_id  # Replace with your WhatsApp group ID (e.g., KUUCaTagxvw1ggpDpBkIeo)
     ```

3. **Ensure Dataset**:
   - Verify that `dataset_menu_30_hari.csv` is in the project directory. No changes are needed unless you want to customize the menu data.

## Running the Bot
1. **Ensure WhatsApp Web is Open**:
   - Open WhatsApp Web (`https://web.whatsapp.com`) in your browser and log in by scanning the QR code with your phone.
   - Keep the browser open while the bot runs, as PyWhatKit uses browser automation.

2. **Run the Bot**:
   - Execute the bot to send messages daily at 05:00 WIB:
     ```bash
     python whatsapp_bot.py
     ```
   - The bot will read `dataset_menu_30_hari.csv` and schedule the first menu to be sent at 05:00 WIB on the start date (default: 2025-07-04). Subsequent messages are sent daily at 05:00 WIB.
   - Check your WhatsApp group for messages sent from your personal WhatsApp account.
   - View logs in `bot.log` for details (e.g., scheduling, sending, errors).

3. **Testing Mode (Optional)**:
   - To test the bot by sending messages every minute, modify the `send_whatsapp_message` function in `whatsapp_bot.py`:
     ```python
     # Replace this:
     pywhatkit.sendwhatmsg_to_group(group_id, message, 5, 0, wait_time=30)
     # With this:
     send_time = datetime.now() + timedelta(minutes=1)
     pywhatkit.sendwhatmsg_to_group(group_id, message, send_time.hour, send_time.minute, wait_time=10)
     ```
   - And modify the `run_menu_bot` loop:
     ```python
     # Replace this:
     send_date = start_date + timedelta(days=index)
     current_date = datetime.now().date()
     if send_date.date() >= current_date:
         logger.info(f"Menjadwalkan pengiriman untuk hari {day} pada {send_date}")
         time_to_wait = (send_date.replace(hour=5, minute=0, second=0) - datetime.now()).total_seconds()
         if time_to_wait > 0:
             logger.info(f"Menunggu {time_to_wait} detik hingga pukul 05:00 WIB")
             time.sleep(time_to_wait)
         send_whatsapp_message(group_id, message, day)
         logger.info(f"Selesai mengirim pesan untuk hari {day}, menunggu 60 detik sebelum lanjut")
         time.sleep(60)
     else:
         logger.info(f"Melewati hari {day} karena tanggal {send_date.date()} sudah lewat")
     # With this:
     send_whatsapp_message(group_id, message, day)
     logger.info(f"Selesai mengirim pesan untuk hari {day}, menunggu 60 detik sebelum lanjut")
     time.sleep(60)
     ```
   - Run the bot again:
     ```bash
     python whatsapp_bot.py
     ```
   - Messages will be sent every ~1 minute for testing.

## Dataset
The dataset (`dataset_menu_30_hari.csv`) contains 30 days of Indonesian recipes with the following columns:
- `Hari`: Day number (1-30)
- `Menu`: Name of the dish
- `Bahan`: Ingredients
- `Bumbu`: Seasonings
- `Harga`: Price in IDR
- `Tutorial`: Cooking instructions

You can customize the dataset by editing `dataset_menu_30_hari.csv` or replacing it with your own CSV file, ensuring the column names remain the same.

## Limitations
- **WhatsApp Web Dependency**: The bot requires WhatsApp Web to be open and logged in with your personal WhatsApp account. Messages will appear as sent from your number.
- **Manual Interaction**: PyWhatKit automates browser actions, which may fail if the browser is closed or WhatsApp Web logs out.
- **Not Fully Automated**: Unlike Twilio or WhatsApp Business API, PyWhatKit cannot send messages from a separate number or without user interaction.
- **Rate Limits**: Sending messages too quickly may trigger WhatsApp's spam detection. The bot includes a 60-second delay between messages to mitigate this.

For fully automated sending from a dedicated number, consider using the Twilio API (see alternative branch or implementation).

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
