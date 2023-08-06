import attr
import json
import os

from typing import List, Optional

from . import Faq
from .constants import CACHE_FAQ_FILEPATH


def faqs_to_json(faqs: List["Faq"]) -> List[dict]:
    return [attr.asdict(faq) for faq in faqs]


def save_faqs(faqs: List["Faq"]):
    faqs_json = faqs_to_json(faqs)
    with open(CACHE_FAQ_FILEPATH, "w") as fp:
        json.dump(faqs_json, fp)


def load_faqs() -> Optional[List["Faq"]]:
    if not os.path.isfile(CACHE_FAQ_FILEPATH):
        return None
    results: List[dict] = list()
    with open(CACHE_FAQ_FILEPATH, "r") as fp:
        results = json.load(fp)
    return [Faq(**dat) for dat in results]
