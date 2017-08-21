import codecs
import os
from textrank4zh import TextRank4Keyword, TextRank4Sentence


class TextRank():
    def __init__(self, source, school):
        file_path = os.getcwd() + '\\data\\raw\\' + source + '\\' + school + '.csv'
        text = codecs.open(file_path, 'r', encoding='utf-8').read()

        self.tr4w = TextRank4Keyword(os.getcwd() + '\\data\\stopwords.txt')
        self.tr4w.analyze(text, lower=True)

    def print_keywords(self, n_top_words=10):
        for item in self.tr4w.get_keywords(n_top_words):
            print(item.word, item.weight)

    def print_keyphrases(self, n_top_phrases=10):
        for phrase in self.tr4w.get_keyphrases(n_top_phrases):
            print(phrase)


if __name__ == '__main__':
    tr = TextRank('zhihu', 'ahu')
    print('keywords:')
    tr.print_keywords(20)
    print('keyphrases:')
    tr.print_keyphrases()