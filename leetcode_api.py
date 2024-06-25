from datetime import datetime

import requests
from pydantic import ValidationError
from requests.exceptions import (HTTPError,
                                 JSONDecodeError,
                                 InvalidJSONError)

from config import config
from models import (Challenge,
                    DailyCodingQuestionRecords)


def get_daily_challenge() -> Challenge:
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

    response = requests.post(config.API_URL,
                             json=payload,
                             headers=headers)

    try:
        daily_records = DailyCodingQuestionRecords(data=response.json()["data"])
    except (HTTPError,
            JSONDecodeError,
            InvalidJSONError) as e:
        raise e
    except ValidationError as e:
        raise e

    challenge = daily_records.data.dailyCodingChallengeV2.challenges[-1]

    return challenge
