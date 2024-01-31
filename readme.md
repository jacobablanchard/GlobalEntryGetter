# Global Entry Getter

![Global entry getter logo](.readmeImages/GlobalEntryGetter.png)

## What does it do?

This program will poll the global entry website to see if there is a newer appointment for Global Entry for you.

Features:

- Checks the global entry website once every minute for a better appointment
- Sends Email notifications
- Sends Pushbullet notifications
- Will not notify you if you have a better appointment
- Even though the app polls once every minute, it won't notify you if it's been less than 15 minutes, and the open timeslot is the same as the one it already notified you for
  - If 15 minutes goes by, and that same slot is open, the app will notify you again
  - If a better appointment than the one you've already been notified for shows up within that 15 minute window, you'll be re-notified

## How do I set it up?

1. Clone the repo
2. In the `.env` file, fill in the following values
   - `SENDER_EMAIL`: Fill this in with the email of the account that will be used to send the email (App has only been tested with Gmail)
   - `RECIPIENT_EMAIL`: Fill this in with the email address of the person who should receive the notification
   - `SMTP_PASSWORD`: Log into the email that you specified in SENDER_EMAIL, then follow [these instructions](https://support.google.com/accounts/answer/185833?hl=en) to generate an app password for your account. Input the value here
   - `PUSHBULLET_TOKEN`: (optional): Will allow you to send Pushbullet notifications to the account that you generate the token for. To generate, log into Pushbullet, then visit (this link)[https://www.pushbullet.com/#settings/account]. Click "Create Access Token", and paste the value into here
3. Install the requirements: `pip install requirements.txt`
4. (If you're trying to get an appointment at another location other then dfw) find the location id of the location that you're trying to get an appointment
   - Find the id [here](https://gist.github.com/mbgearhead/64c2c1d1ed0956df6974512305aa98aa) for the location you're trying to book
   - Add it to `known_location_ids` in `main.py`
   - In `main.py`, set `location_of_interest` to the id of the location you're interested in
5. Run the app! `python3 main.py`

The app will poll the global entry website for a better appointment than what's specified in `main.py` in the `current_best_appointment` variable. If you manage to snag a better appointment, simply update this variable, then re-start the app.
