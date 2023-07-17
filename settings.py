from dotenv import load_dotenv
import os

load_dotenv()

sender = os.getenv("SENDER_EMAIL")
recipients = [os.getenv("RECIPIENT_EMAIL")]
password = os.getenv("SMTP_PASSWORD")
pushbullet_token = os.getenv("PUSHBULLET_TOKEN")
