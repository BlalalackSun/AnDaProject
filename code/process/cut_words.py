# coding:utf-8
import os
import jieba
import pprint



def cut_words(source, school):
    src_path = os.getcwd() + '\\data\\raw\\' + source + '\\' + school + '.csv'
    dest_path = os.getcwd() + '\\data\\cutted\\' + source + '\\' + school

    with open(dest_path, 'w', encoding='utf-8') as dest_file:
        with open(src_path, 'r', encoding='utf-8') as src_file:
            for line in src_file:
                words = jieba.cut(line.strip())
                dest_file.write(' '.join(words)) # 最后所有行的文本，变成一行被分词的语料


if __name__ == '__main__':
    cut_words('tieba', 'ahu')
