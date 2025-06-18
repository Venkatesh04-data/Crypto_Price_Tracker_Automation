import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.blocking import BlockingScheduler

# ----- CONFIGURATION -----
CRYPTO = "bitcoin"
CURRENCY = "usd"
ALERT_THRESHOLD = 70000  # Set your threshold

TO_EMAIL = "venkatesh.gudade04@gmail.com"
FROM_EMAIL = "venkatesh.gudade04@gmail.com"
APP_PASSWORD = "hsth dqep zfip bcoo"  # Use Gmail App Password

CSV_FILE = "prices.csv"

# ----- FUNCTIONS -----

def fetch_price():
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={CRYPTO}&vs_currencies={CURRENCY}"
        response = requests.get(url)
        return response.json()[CRYPTO][CURRENCY]
    except Exception as e:
        print("❌ Error fetching price:", e)
        return None

def save_to_csv(price):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame([[now, price]], columns=["Timestamp", "Price"])
    try:
        df.to_csv(CSV_FILE, mode='a', header=not pd.io.common.file_exists(CSV_FILE), index=False)
        print(f"✅ Logged: {now} → ${price}")
    except Exception as e:
        print("❌ Error saving to CSV:", e)

def send_email_alert(subject, body, to_email, from_email, app_password):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, app_password)
        server.send_message(msg)
        server.quit()
        print("📧 Email sent!")

    except Exception as e:
        print("❌ Failed to send email:", e)

def check_alert(price):
    if price >= ALERT_THRESHOLD:
        send_email_alert(
            subject="🚨 Bitcoin Price Alert!",
            body=f"Bitcoin is at ${price} — above your threshold of ${ALERT_THRESHOLD}.",
            to_email=TO_EMAIL,
            from_email=FROM_EMAIL,
            app_password=APP_PASSWORD
        )

def track_and_alert():
    print("🔄 Running scheduled check...")
    price = fetch_price()
    if price:
        save_to_csv(price)
        check_alert(price)

# ----- SCHEDULER -----
if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(track_and_alert, 'interval', minutes=10)
    print("🚀 Crypto Price Tracker started! Checking every 10 minutes...\n")
    scheduler.start()
