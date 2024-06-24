import datetime
import time

import pytz
from scheduler import Scheduler
import requests
from leetcode_api import get_daily_challenge
from models import DailyCodingChallenge
from os import getenv
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(getenv("CHAT_ID"))
TIMEZONE = getenv("TIMEZONE")


def get_message_text(challenge: DailyCodingChallenge) -> str:
    message_elements = [
        f"<b>New LeetCode Daily Challenge!</b>",
        f"",
        f"<b>{challenge.question.title} [{challenge.question.difficulty}]</b>",
        f"",
        f"<b>Link: leetcode.com{challenge.link}</b>"
    ]

    return "\n".join(message_elements)


def daily_task() -> None:
    today_challenge = get_daily_challenge()

    message_text = get_message_text(today_challenge)

    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                  json={
                      "chat_id": CHAT_ID,
                      "text": message_text,
                      "parse_mode": "HTML",
                      "link_preview_options": {
                          "is_disabled": True
                      }
                  })


if __name__ == "__main__":
    schedule = Scheduler()

    schedule.daily(datetime.time(hour=8, minute=30, tzinfo=pytz.timezone(TIMEZONE)),
                   daily_task)

    while True:
        schedule.exec_jobs()
        time.sleep(1)
