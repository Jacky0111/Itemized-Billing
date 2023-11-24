import enchant


class TextTransformation():
    def __init__(self, df):
        self.df = df
        self.dict = enchant.Dict('en_US')

    def spellCheck(self, col):
        self.df[col] = self.df[col].apply(self.correct_spelling)
        return self.df

    def correct_spelling(self, text):
        if text is not None:
            return ' '.join(self.correct_word(word) for word in str(text).split())
        else:
            return text

    # def correct_word(self, word):
    #     return self.dict.suggest(word)[0] if not self.dict.check(word) else word

    def correct_word(self, word):
        if not self.is_english_word(word):
            suggestions = self.dict.suggest(word)
            return suggestions[0] if suggestions else word
        else:
            return word

    def is_english_word(self, word):
        return self.dict.check(word)



