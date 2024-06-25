import datetime
import time

import pytz
import telebot
from scheduler import Scheduler

from config import config
from leetcode_api import get_daily_challenge
from models import Challenge


def get_message_text(challenge: Challenge) -> str:
    message_elements = [
        f"<b>New LeetCode Daily Challenge!</b>",
        f"",
        f"<b>{challenge.question.title} [{challenge.question.difficulty}]</b>",
        f"",
        f"<b>Link: leetcode.com{challenge.link}</b>"
    ]

    return "\n".join(message_elements)


def daily_task() -> None:
    bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN.get_secret_value(),
                          parse_mode="HTML",
                          disable_web_page_preview=True)

    today_challenge = get_daily_challenge()

    message_text = get_message_text(today_challenge)

    bot.send_message(chat_id=config.CHAT_ID,
                     text=message_text)


if __name__ == "__main__":
    schedule = Scheduler(tzinfo=datetime.timezone.utc)
    config_timezone = pytz.timezone(config.TIMEZONE)

    schedule.daily(datetime.time(hour=8,
                                 minute=30,
                                 tzinfo=config_timezone),
                   daily_task)

    start_time = datetime.datetime.now(tz=config_timezone)

    if not (start_time.hour <= 8 and start_time.minute <= 30):
        daily_task()

    while True:
        schedule.exec_jobs()
        time.sleep(1)
