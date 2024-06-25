from pydantic import BaseModel


class Question(BaseModel):
    title: str
    titleSlug: str
    difficulty: str


class Challenge(BaseModel):
    date: str
    link: str
    question: Question

    def __post_model_init__(self,
                            __context):
        self.link = self.link[:-1] if self.link[-1] == "/" else self.link


class DailyCodingChallengeV2(BaseModel):
    challenges: list[Challenge]


class Data(BaseModel):
    dailyCodingChallengeV2: DailyCodingChallengeV2


class DailyCodingQuestionRecords(BaseModel):
    data: Data
