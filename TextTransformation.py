from spellchecker import SpellChecker


class TextTransformation():
    def __init__(self, df):
        self.df = df

    def spellCheck(self, col):
        spell = SpellChecker()
        self.df[col] = self.df[col].apply(lambda x: ' '.join(
            spell.correction(word) if (word is not None and spell.correction(word) is not None) else str(word) for word
            in str(x).split()))
        return self.df