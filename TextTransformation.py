import enchant
from spellchecker import SpellChecker


class TextTransformation():
    def __init__(self, df):
        self.df = df
        self.dict = enchant.Dict('en_US')

    # def spellCheck(self, col):
    #     spell = SpellChecker()
    #     self.df[col] = self.df[col].apply(lambda x: ' '.join(
    #         spell.correction(word) if (word is not None and spell.correction(word) is not None) else str(word) for word
    #         in str(x).split()))
    #     return self.df

    def spellCheck(self, col):
        self.df[col] = self.df[col].apply(self.correct_spelling)
        return self.df

    def correct_spelling(self, text):
        return ' '.join(self.correct_word(word) for word in text.split())

    # def correct_word(self, word):
    #     return self.dict.suggest(word)[0] if not self.dict.check(word) else word

    def correct_word(self, word):
        suggestions = self.dict.suggest(word)
        return suggestions[0] if suggestions else word


