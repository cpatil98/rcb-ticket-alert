import requests
from bs4 import BeautifulSoup
import time
import os
import telegram

# -------------------------------
# Environment variables (safer)
# Set these in your system or Render)
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Telegram bot token
CHAT_ID = os.getenv("CHAT_ID")      # Your Telegram chat ID
# -------------------------------

# Telegram setup
bot = telegram.Bot(token=BOT_TOKEN)

# RCB ticket page URL
URL = "https://shop.royalchallengers.com/ticket"

# Interval between checks (seconds)
CHECK_INTERVAL = 30

def send_telegram(message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"✅ Alert sent: {message}")
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")

def check_tickets():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(URL, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text().lower()

        # Look for keywords indicating tickets are live
        if "ticket" in page_text and ("buy" in page_text or "book" in page_text):
            send_telegram(f"🔥 RCB Tickets are LIVE! {URL}")
            return True
        else:
            print("🔍 Checking for RCB tickets... ❌ Not live yet...")
            return False

    except Exception as e:
        print(f"❌ Error checking tickets: {e}")
        return False

if __name__ == "__main__":
    while True:
        if check_tickets():
            break  # stop script after sending alert
        time.sleep(CHECK_INTERVAL)