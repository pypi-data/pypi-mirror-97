from enum import Enum


CATEGORIES = (
    "milf",
    "hentai",
    "ecchi"
)


class Result:
    def __init__(self, data: dict):
        self.url = data.get("url")
