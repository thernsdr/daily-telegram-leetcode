class Question:
    def __init__(self, title, title_slug, difficulty):
        self.title: str = title
        self.title_slug: str = title_slug
        self.difficulty: str = difficulty


class DailyCodingChallenge:
    def __init__(self, date, link, question):
        self.date: str = date
        self.link: str = link if link[-1] != "/" else link[:-1]
        self.question: Question = question
