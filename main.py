import logging
import os
import re

import requests

TARGET_AGE = int(os.getenv("TARGET_AGE"))
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
RECIPIENT = os.getenv("RECIPIENT")

NHS_URL = "https://www.nhs.uk/conditions/coronavirus-covid-19/coronavirus-vaccination/book-coronavirus-vaccination/"


class RequestFailureError(Exception):
    pass


def find_current_nhs_age():
    regex = "aged (\d+) or over"
    response = requests.get(NHS_URL)
    if response.status_code == 200:
        result = re.search(regex, response.text, re.IGNORECASE)
        return int(result.group(1))
    else:
        raise RequestFailureError(f"Failed to connect to ${NHS_URL}")


def notify():
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": f"COVID Vaccine Notifier <mailgun@{MAILGUN_DOMAIN}>",
              "to": [RECIPIENT],
              "subject": f"COVID Vaccine Is Available For {TARGET_AGE} Year Olds!",
              "text": f"MyNameIsMikeGreen's COVID vaccine notifier has detected that the COVID vaccine is now available to those aged {TARGET_AGE} years old!\n\nBook here: {NHS_URL}\n\nProject: https://github.com/MyNameIsMikeGreen/covid-vaccine-notifier/"
              })
    if response.status_code == 200:
        logging.info("Notification sent!")
    else:
        logging.info(f"HTTP {response.status_code}: {response.text}")
        raise RequestFailureError("Failed to send notification")


def main():
    current_nhs_age = find_current_nhs_age()
    logging.info(f"Target age set to: {TARGET_AGE}")
    logging.info(f"Detected current COVID vaccine age threshold as: {current_nhs_age}")
    if current_nhs_age <= TARGET_AGE:
        logging.info("Sending notification...")
        notify()
    else:
        logging.info(f"Vaccine not available for {TARGET_AGE} year olds yet :(")


if __name__ == '__main__':
    logging.basicConfig(filename='covidVaccineNotifier.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S')
    main()
