from datetime import datetime

import requests

from models import Question, DailyCodingChallenge

API_URL = "https://leetcode.com/graphql/"


def get_daily_challenge() -> DailyCodingChallenge:
    year = datetime.now().year
    month = datetime.now().month

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"
    }

    query = """
    query dailyCodingQuestionRecords($year: Int!, $month: Int!) {
      dailyCodingChallengeV2(year: $year, month: $month) {
        challenges {
          date
          link
          question {
            title
            titleSlug
            difficulty
          }
        }
      }
    }
    """

    variables = {
        "year": year,
        "month": month
    }

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    data = response.json()

    challenge = data["data"]["dailyCodingChallengeV2"]["challenges"][-1]

    question = Question(
        title=challenge["question"]["title"],
        title_slug=challenge["question"]["titleSlug"],
        difficulty=challenge["question"]["difficulty"]
    )

    daily_challenge = DailyCodingChallenge(
        date=challenge["date"],
        link=challenge["link"],
        question=question
    )

    return daily_challenge
