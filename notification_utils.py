import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

from Appointment import Appointment

subject = "New Appointment Found"

sender = os.getenv("SENDER_EMAIL")
recipients = [os.getenv("RECIPIENT_EMAIL")]
password = os.getenv("SMTP_PASSWORD")


def send_notification(current_appointment: datetime, better_appointment: Appointment):
    body = f"There's a new appointment available for you:\nCurrent Appointment: {current_appointment:%A, %B %d %Y @ %I:%M %p}\nFound Appointment:{better_appointment.startTimestamp:%A, %B %d %Y @ %I:%M %p}\nOther data: {better_appointment}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")
