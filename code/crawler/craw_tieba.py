# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import pprint
import re
import random



class TieBa():
    def __init__(self):
        self.folder = os.getcwd() + '\\data\\raw\\tieba\\'
        self.driver = webdriver.Firefox()


    # 一个具体高校的贴吧看帖是以pn=num 来索引下一页，每一页pn增长的步长是50，如下所示第一页，第二页url
    # http://tieba.baidu.com/f?kw=%E5%AE%89%E5%BE%BD%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=0
    # http://tieba.baidu.com/f?kw=%E5%AE%89%E5%BE%BD%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=50
    def access(self, school, base_url, step=50):
        print('School:' + school)
        
        cookie = self.driver.get_cookies()
        time.sleep(2)
        
        page_idx = 0
        self.driver.get(base_url + str(int(page_idx*step)))
        time.sleep(3)

        while True:
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            current_page_num = soup.find('span', {'class':'pagination-current pagination-item '}).get_text()
            print('-'*10,'Browse posts, page number:' + current_page_num,'-'*10)

            # 获取看帖的一个页面
            posts = self._get_posts_url_in_page(soup)
            # 访问与存储该页面中的所有帖子
            for rep_num, post_url in posts:
                print(rep_num, post_url)
                self._access_post(post_url)

            if '下一页' in soup.find('div', {'class':'pagination-default clearfix'}).get_text():
                # if page_idx >= 2: # for test
                #     break
                
                page_idx += 1
                self.driver.get(base_url + str(int(page_idx*step)))
                time.sleep(3)
            else:
                break
                
        print('Finished the last page...')
        

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

        title = soup.find('h1', {'class':'core_title_txt'}).get_text()
        title = self._clean(title)
        contents = []

        page_idx = 1
        while True:
            print('In post, page number:' + str(page_idx))

            for floor in soup.find_all('cc'):
                floor_content = self._clean(floor.div.get_text())
                # print(floor_content)
                contents.append(floor_content)


            if '下一页' in soup.find('li', {'class':'l_pager pager_theme_4 pb_list_pager'}).get_text() \
                and page_idx <= max_pages:

                page_idx += 1
                next_page_url = post_url + '?pn=' + str(page_idx)
                wrong_times = 0
                while True:
                    try:
                        self.driver.get(next_page_url)
                        html = self.driver.page_source
                        soup = BeautifulSoup(html)
                        break
                    except:
                        if wrong_times >= 3:
                            print('Wrong too many in ' + next_page_url + ', abandon the post...')
                            return
                        wrong_times += 1
                        print('Something wrong while access ' + next_page_url)
                        print('Wait a moment...')
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
        'ahu':'http://tieba.baidu.com/f?kw=%E5%AE%89%E5%BE%BD%E5%A4%A7%E5%AD%A6&ie=utf-8&pn='
        # 在这里添加学校缩写和贴吧首页url
    }
    
    tb = TieBa()
    for school, url in school_base_url.items():        
        time_begin = time.time()
        tb.access(school, url)
        time.sleep(5)
        time_end = time.time()
        print('Cost time in {0} is {1} seconds.'.format(school, str(time_end-time_begin)))


# 