import json
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
import logging
import requests
from settings import password, pushbullet_token, recipients, sender
from Appointment import Appointment

logger = logging.getLogger(__name__)
subject = "New Appointment Found"


def send_notification(current_appointment: datetime, better_appointment: Appointment):
    body = (
        f"There's a new appointment available for you:\n"
        f"Current Appointment: {current_appointment:%A, %B %d %Y @ %I:%M %p}\n"
        f"Found Appointment:{better_appointment.startTimestamp:%A, %B %d %Y @ %I:%M %p}\n"
        f"Other data: {better_appointment}\n\n"
        f"https://ttp.cbp.dhs.gov/"
    )
    if all(map(lambda p: p is not None, [sender, recipients, password])):
        send_email(body)
    else:
        logger.info("Not sending email due to missing email config")

    if pushbullet_token:
        send_pushbullet_notification(body)
    else:
        logger.info("Not sending push due to missing pushbullet config")


def send_email(bodyText: str):
    msg = MIMEText(bodyText)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())


def send_pushbullet_notification(bodyText: str):
    url = "https://api.pushbullet.com/v2/pushes"

    r = requests.post(
        url,
        data=json.dumps({"type": "note", "title": subject, "body": bodyText}),
        headers={"Access-Token": pushbullet_token, "Content-type": "application/json"},
    )
