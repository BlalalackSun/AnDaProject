# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import pprint
import re
import random
import logging


logger = logging.getLogger('tieba_log')
logger.setLevel(logging.INFO)


class TieBa():
    def __init__(self):
        self.folder = os.getcwd() + '\\data\\raw\\tieba\\'
        self.log_folder = os.getcwd() + '\\data\\logs\\tieba\\'
        self.driver = webdriver.Firefox()

    # 一个具体高校的贴吧看帖是以pn=num 来索引下一页，每一页pn增长的步长是50，如下所示第一页，第二页url
    # http://tieba.baidu.com/f?kw=%E5%AE%89%E5%BE%BD%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=0
    # http://tieba.baidu.com/f?kw=%E5%AE%89%E5%BE%BD%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=50
    def access(self, school, base_url, page_idx=0, step=50):
        # ---------log init---------
        fh = logging.FileHandler(self.log_folder + school + '.log')
        fh.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s   %(message)s', datefmt='%y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)
        # ---------log init ---------
        
        cookie = self.driver.get_cookies()
        time.sleep(2)
        
        self.driver.get(base_url + str(int(page_idx*step)))
        time.sleep(5)

        while True:
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            current_page_num = soup.find('span', {'class':'pagination-current pagination-item '}).get_text()
            logger.info('Browse posts, page number:' + current_page_num)

            # 获取看帖的一个页面
            posts = self._get_posts_url_in_page(soup)
            # 访问与存储该页面中的所有帖子
            for rep_num, post_url in posts:
                logger.info('\t' + str(rep_num) + ' ' + post_url)
                self._access_post(post_url)

            if '下一页' in soup.find('div', {'class':'pagination-default clearfix'}).get_text():
                page_idx += 1
                next_posts_page_url = base_url + str(int(page_idx*step))
                wrong_times = 0
                while True:
                    try:
                        self.driver.get(next_posts_page_url)
                        time.sleep(2)
                        break
                    except:
                        if wrong_times >= 3:
                            logger.info('\t' + 'Wrong too many in "{}", abandon it'.format(next_posts_page_url))
                            page_idx += 1
                            next_posts_page_url = base_url + str(int(page_idx*step))
                            self.driver.get(next_posts_page_url)
                            time.sleep(2)
                            break
                        wrong_times += 1
                        logger.info('\tSomething wrong while access post:' + next_posts_page_url)
                        logger.info('Wait a moment...')
                        time.sleep(random.randint(20, 100))

            else:
                break
                
        logger.info('Done...')
        # ---------log free----------
        logger.removeHandler(ch)
        logger.removeHandler(fh)
        # ---------log free----------

    # 返回当前页面中帖子的回复数以及帖子的链接构成的元组的列表, eg:
    # [(469, 'http://tieba.baidu.com/p/5223883150'), (0, 'http://tieba.baidu.com/p/3455737547'), ...]
    def _get_posts_url_in_page(self, page_soup):
        tieba_url = 'http://tieba.baidu.com'
        post_list = []

        for post in page_soup.findAll('div', {'class':'t_con cleafix'}):
            rep_num = post.find('span', {'class':'threadlist_rep_num center_text'}).get_text()
            post_url = tieba_url + post.find('a', {'class':'j_th_tit'})['href']

            # 同时发布到其他贴吧的url，会以 ?fid=4631 结尾，忽略这种url，方便处理
            if '?fid=4631' in post_url:
                continue
            post_list.append((rep_num, post_url))

        return post_list


    # 获取一个帖子的标题和所有楼层数据(最多取max_pages页数据，默认最多50页)
    # 对帖子的存储数据格式为csv，eg：
    # title,floor1 floor2 floor3...
    def _access_post(self, post_url, max_pages=50):
        self.driver.get(post_url)
        time.sleep(3)

        html = self.driver.page_source
        soup = BeautifulSoup(html)

        try:
            title = soup.find('h1', {'class':'core_title_txt'}).get_text()
            title = self._clean(title)
        except:
            logger.info('\t'*2 + 'No title in this page, abandon it')
            return


        contents = []

        page_idx = 1
        while True:
            logger.info('\t'*2 + 'In post, page number:' + str(page_idx))

            for floor in soup.find_all('cc'):
                floor_content = self._clean(floor.div.get_text())
                contents.append(floor_content)


            if '下一页' in soup.find('li', {'class':'l_pager pager_theme_4 pb_list_pager'}).get_text() \
                and page_idx <= max_pages:

                page_idx += 1
                next_page_url = post_url + '?pn=' + str(page_idx)
                wrong_times = 0
                while True:
                    try:
                        self.driver.get(next_page_url)
                        time.sleep(1)
                        html = self.driver.page_source
                        soup = BeautifulSoup(html)
                        break
                    except:
                        if wrong_times >= 3:
                            logger.info('\t'*2 + 'Wrong too many in ' + next_page_url + ', abandon the post...')
                            return
                        wrong_times += 1
                        logger.info('\t'*2 + 'Something wrong while access ' + next_page_url)
                        logger.info('\t'*2 + 'Wait a moment...')
                        time.sleep(random.randint(20, 100))
            else:
                break

        # 数据加入文件
        # 格式：title,floor1 floor2 floor3 ...
        with open(self.folder + school + '.csv', 'a', encoding='utf-8') as f:
            f.write(title + ',' + ' '.join(contents) + '\n')
            

    def _clean(self, text):
        # 因为要用英文的逗号,作为csv文件的分隔符，所以对于问题或答案中的英文,转成中文逗号，避免对csv文件造成影响
        text = re.sub(r',', '，', text)
        # 清理换行符，改成空格
        text = re.sub(r'\n', ' ', text)
        # 连续的空白符换成单个空格
        text = re.sub(r'\s+', ' ', text)
        # 将文本中的超链接换成空格，避免标签对结果影响(never try this change)
        text = re.sub(r'((http|ftp|https):\/\/)[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', ' ', text)
        return text



if __name__ == '__main__':
    school_base_url = {
        # 'ahu':('http://tieba.baidu.com/f?kw=%E5%AE%89%E5%BE%BD%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=',110),
        # 'pku':('http://tieba.baidu.com/f?kw=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=',130),
        # 'thu':('http://tieba.baidu.com/f?kw=%E6%B8%85%E5%8D%8E%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=', 102),
        # 'nju':('http://tieba.baidu.com/f?kw=%E5%8D%97%E4%BA%AC%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=', 83)
        'zju':('http://tieba.baidu.com/f?kw=%E6%B5%99%E6%B1%9F%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=', 3)
        # 在这里添加学校缩写和贴吧首页base_url
    }
    
    tb = TieBa()
    for school, url_and_idx in school_base_url.items():        
        tb.access(school, url_and_idx[0], url_and_idx[1])
        time.sleep(5)