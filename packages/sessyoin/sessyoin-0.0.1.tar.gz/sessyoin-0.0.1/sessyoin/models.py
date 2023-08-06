from enum import Enum


CATEGORIES = (
    "ass",
    "bikini",
    "boots",
    "cleavage",
    "glasses",
    "kemonomimi",
    "maid",
    "panties",
    "thigh"
)


class Result:
    def __init__(self, data: dict):
        self.url = data.get("url")
