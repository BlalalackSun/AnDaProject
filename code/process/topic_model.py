# coding: utf-8
import pandas as pd
import jieba
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from pprint import pprint
import os
import numpy as np


class LDA():
    def __init__(self, source, school):
        file_path = os.getcwd() + '\\data\\' + source + '\\' + school + '.csv'
        # 爬取数据时，每一行数据都是一个二元组，意义随数据来源稍有不同
        # 知乎(question, answer), 贴吧(title, floors), ...
        # 这里用(title, content)进行统一
        self.df = pd.read_csv(file_path, names=['title', 'content'])
        self.stopwords = codecs.open(os.getcwd() + '\\data\\stopwords.txt', 'r', encoding='utf-8')
        self.stopwords = [w.strip() for w in self.stopwords]
        
        self.lda = None
        self.tf_vectorizer = None


    def run_lda(self, n_topics=5):
        def chinese_word_cut(text):
            return ' '.join(jieba.cut(text))

        self.df['content_cutted'] = self.df.content.apply(chinese_word_cut)
        self.tf_vectorizer = CountVectorizer(strip_accents='unicode', stop_words=self.stopwords)
        tf = self.tf_vectorizer.fit_transform(self.df.content_cutted)

        self.lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50, \
                learning_method='online', learning_offset=50, random_state=0)
        self.lda.fit(tf)


    def print_top_word(self, n_top_words=10):
        # pprint(self.lda.components_ / self.lda.components_.sum(axis=1)[:, np.newaxis])

        tf_feature_names = self.tf_vectorizer.get_feature_names()
        for topic_idx, topic in enumerate(self.lda.components_):
            print('Topic #{0}:'.format(str(topic_idx)))
            print(' '.join([tf_feature_names[i] for i in topic.argsort()[:-n_top_words-1:-1]]))
            print()



if __name__ == '__main__':
    topic_model = LDA('zhihu', 'ahu')
    topic_model.run_lda()
    topic_model.print_top_word()
    