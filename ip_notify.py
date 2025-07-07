import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env in same folder
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", SENDER_EMAIL)

def get_public_ip():
    try:
        return requests.get("https://api64.ipify.org", timeout=5).text.strip()
    except Exception as e:
        print(f"[ERROR] Could not get public IP: {e}")
        return None

def send_email(ip):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = "Public IP Changed"
    msg.attach(MIMEText(f"New public IP: {ip}", "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        print("[OK] Email sent.")
    except Exception as e:
        print(f"[ERROR] Email failed: {e}")

def main():
    current_ip = get_public_ip()
    if not current_ip:
        return

    ip_file = "/tmp/last_ip.txt"
    last_ip = None

    if os.path.exists(ip_file):
        with open(ip_file, "r") as f:
            last_ip = f.read().strip()

    if current_ip != last_ip:
        send_email(current_ip)
        with open(ip_file, "w") as f:
            f.write(current_ip)
    else:
        print("[SKIP] IP unchanged.")

if __name__ == "__main__":
    main()
