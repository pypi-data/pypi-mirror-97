import requests
import logging
from fuzzywuzzy import process
from typing import List

from . import Faq, Tiket
from .utils import save_faqs, load_faqs


class HalloUt:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.faqs = self.load_faqs()
        self.faq_q_dict = dict(enumerate([faq.question for faq in self.faqs]))

    def __call__(self, query: str, limit: int = 10) -> List[Faq]:
        return self.faq(query, limit)

    def faq(self, query: str, limit: int = 10, score_cutoff: int = 60) -> List[Faq]:
        self.logger.debug(f"Mencari faq dengan keyword `{query}`")
        best_faq = process.extractBests(
            query, self.faq_q_dict, score_cutoff=score_cutoff, limit=10
        )
        self.logger.debug(f"Ditemukan {len(best_faq)} kemungkinan jawaban")
        return [self.faqs[z] for (x, y, z) in best_faq] if best_faq else []

    def status_tiket(self, noticket: str) -> Tiket:
        return Tiket.from_noticket(noticket=noticket)

    @staticmethod
    def load_faqs() -> List[Faq]:
        faqs = load_faqs()
        if faqs:
            return faqs
        faqs = Faq.fetch_faqs()
        save_faqs(faqs)
        return faqs
