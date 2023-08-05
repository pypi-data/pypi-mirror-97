from typing import List


class ProfanityChecker:

    def __init__(self, profane_words: List[str]):
        self.profane_words = profane_words

    def get_profane_words(self, words_list: List[str]) -> List:
        return [word for word in words_list if self.is_profane(word)]

    def is_profane(self, word: str) -> bool:
        return self.normalize_word(word) in self.profane_words

    @classmethod
    def normalize_word(cls, word: str):
        return word.lower()
