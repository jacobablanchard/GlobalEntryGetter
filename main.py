import logging
import logging.config
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta

import requests
import schedule

from Appointment import Appointment
from notification_utils import send_notification
from persistence import ProgramData
from dotenv import load_dotenv

load_dotenv()


logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standardFormatter": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        },
    },
    "handlers": {
        "stdoutHandler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standardFormatter",
            "stream": sys.stdout,
        },
        "contactHandler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "standardFormatter",
            "filename": "contactLog.log",
            "mode": "w",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["stdoutHandler"],
    },
    "loggers": {
        "urllib3.connectionpool": {
            "level": "DEBUG",
            "handlers": ["stdoutHandler"],
            "propagate": False,
        },
        "contactLogger": {
            "level": "DEBUG",
            "handlers": ["stdoutHandler", "contactHandler"],
            "propagate": False,
        },
    },
}

# Load the logging configuration from dictionary
logging.config.dictConfig(logging_config)

base_url = "https://ttp.cbp.dhs.gov/schedulerapi/slot-availability"
current_best_appointment = datetime.max

logger = logging.getLogger(__name__)
contactLogger = logging.getLogger("contactLogger")


def should_send_notification(
    possible_appointment_datetime: datetime, previous_notification: ProgramData
):
    """
    Dont send notification if:
        * We already have a better appointment
        * We sent the last notification < 15 minutes ago, and the time available is still the same
    """
    if possible_appointment_datetime > current_best_appointment:
        return False

    if (
        datetime.now() - previous_notification.last_notification_sent
        < timedelta(minutes=15)
        and previous_notification.appointment == possible_appointment_datetime
    ):
        return False

    return True


def check_appointment_availability():
    # Send a GET request to the Global Entry site
    logging.info("Running")
    known_location_ids = {"dfw": 5300, "arizona": 8100, "anchorage": 7540}
    response = requests.get(
        base_url,
        params={"locationId": known_location_ids["dfw"]},
    ).json()
    if len(response["availableSlots"]) == 0:
        return
    possible_appointments = [
        Appointment.from_dict(appt) for appt in response["availableSlots"]
    ]
    possible_appointments = sorted(
        possible_appointments, reverse=True, key=lambda x: x.startTimestamp
    )
    logger.info(f"Best appointment available: {possible_appointments[0]}")
    previous_notification = ProgramData.load_from_disk()

    if previous_notification is None or should_send_notification(
        possible_appointments[0].startTimestamp, previous_notification.appointment
    ):
        contactLogger.info(
            f"Sending contact. Current appointment: {current_best_appointment}, Found Appointment: {possible_appointments[0]}"
        )
        send_notification(current_best_appointment, possible_appointments[0])
        if previous_notification is None:
            previous_notification = ProgramData()
        previous_notification.last_notification_sent = datetime.now()
        previous_notification.appointment = possible_appointments[0]
        previous_notification.to_disk()


schedule.every(5).minutes.do(check_appointment_availability)

if __name__ == "__main__":
    # check_appointment_availability()
    schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(1)
