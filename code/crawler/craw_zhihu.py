# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import os
import pprint
import re
from bs4 import BeautifulSoup



class ZhiHu():
    def __init__(self):
        self.folder = os.getcwd() + '\\data\\raw\\zhihu\\'
        self.driver = webdriver.Firefox()    

    def access(self, school, urls):        
        print('School:' + school + ', total ' + str(len(urls)) + ' urls')
        all_ques_ans = set()
        url_idx = 1

        for url in urls:
            cookie = self.driver.get_cookies()
            time.sleep(3)

            print('Get from:' + url)
            self.driver.get(url)
            time.sleep(2)

            # 加载HTML
            click_cnt = 1
            limit_click_cnt = 10
            while True:
                try:
                    self.driver.find_element_by_css_selector('.zg-btn-white.zu-button-more').click()
                    time.sleep(2)
                    print('click:' + str(click_cnt))
                    click_cnt += 1
                    # if click_cnt > limit_click_cnt: # avoid at this while too long or something wrong
                    #     break
                except:
                    break


            # 解析HTML
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            for item in soup.find_all('li', {'class':'item clearfix', 'data-type':'Answer'}):
                ques = item.find('a', {'class':'js-title-link', 'target':'_blank'})
                author = item.find('a', {'class':'author author-link'})
                answer = item.find('script', {'type':'text', 'class':'content'})
                votes = item.find('span', {'class':'count'})

                # 数据清洗
                # 每个问答一行，要消除问与答中的换行
                # 因为要用英文的逗号,作为csv文件的分隔符，所以对于问题或答案中的英文,转成中文逗号，避免对csv文件造成影响
                # 将回答中的超链接换成空格，避免其对文本数据的影响
                answer_text = answer.get_text()
                pure_answer_text = re.sub(r'<.*?>', ' ', answer_text)
                pure_answer_text = re.sub(r',', '，', pure_answer_text)
                pure_answer_text = re.sub(r'\n', ' ', pure_answer_text)
                pure_question_text = re.sub(r',', '，', ques.get_text())
                pure_question_text = re.sub(r'\n', ' ', pure_question_text)

                all_ques_ans.add(pure_question_text + ',' + pure_answer_text)
            
            print('The ' + str(url_idx) + '/' + str(len(urls)) + ' has done...')
            url_idx += 1

        # 数据写入文件
        # 格式：question,answer
        with open(self.folder + school +'.csv', 'w', encoding='utf-8') as f:
            for ques_ans in all_ques_ans:
                f.write(ques_ans + '\n')

        print('Total ' + str(len(all_ques_ans)) + ' lines')
        print('Done...')    



if __name__ == '__main__':
    school_urls = {
        # 'ahu':['https://www.zhihu.com/search?type=content&q=%E5%AE%89%E5%A4%A7',
            #    'https://www.zhihu.com/search?type=content&q=%E5%AE%89%E5%BE%BD%E5%A4%A7%E5%AD%A6']
        'pku':['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E5%A4%A7',
        'https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6']
        # 在这里添加其他学校的缩写与相关关键词的链接    
    }
    
    zh = ZhiHu()
    for school, urls in school_urls.items():
        zh.access(school, urls)
        time.sleep(2)



# 安大,https://www.zhihu.com/search?type=content&q=%E5%AE%89%E5%A4%A7
# 安徽大学,https://www.zhihu.com/search?type=content&q=%E5%AE%89%E5%BE%BD%E5%A4%A7%E5%AD%A6
# 合工大,https://www.zhihu.com/search?type=content&q=%E5%90%88%E5%B7%A5%E5%A4%A7
# 合肥工业大学,https://www.zhihu.com/search?type=content&q=%E5%90%88%E8%82%A5%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6
# 中科大,https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E7%A7%91%E5%A4%A7
# 中国科技大学,https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6
# 清华,https://www.zhihu.com/search?type=content&q=%E6%B8%85%E5%8D%8E
# 清华大学,https://www.zhihu.com/search?type=content&q=%E6%B8%85%E5%8D%8E%E5%A4%A7%E5%AD%A6
# 北大,https://www.zhihu.com/search?type=content&q=%E5%8C%97%E5%A4%A7
# 北京大学,https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6
# 复旦,https://www.zhihu.com/search?type=content&q=%E5%A4%8D%E6%97%A6
# 复旦大学,https://www.zhihu.com/search?type=content&q=%E5%A4%8D%E6%97%A6%E5%A4%A7%E5%AD%A6
# 上交,https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E4%BA%A4
# 上海交通大学,https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E6%B5%B7%E4%BA%A4%E9%80%9A%E5%A4%A7%E5%AD%A6
# 浙大,https://www.zhihu.com/search?type=content&q=%E6%B5%99%E5%A4%A7
# 浙江大学,https://www.zhihu.com/search?type=content&q=%E6%B5%99%E6%B1%9F%E5%A4%A7%E5%AD%A6
# 南大,https://www.zhihu.com/search?type=content&q=%E5%8D%97%E5%A4%A7
# 南京大学,https://www.zhihu.com/search?type=content&q=%E5%8D%97%E4%BA%AC%E5%A4%A7%E5%AD%A6


# '安大':'https://www.zhihu.com/search?type=content&q=%E5%AE%89%E5%A4%A7',
# '安徽大学':'https://www.zhihu.com/search?type=content&q=%E5%AE%89%E5%BE%BD%E5%A4%A7%E5%AD%A6',
# '合工大':'https://www.zhihu.com/search?type=content&q=%E5%90%88%E5%B7%A5%E5%A4%A7',
# '合肥工业大学':'https://www.zhihu.com/search?type=content&q=%E5%90%88%E8%82%A5%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6',
# '中科大':'https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E7%A7%91%E5%A4%A7',
# '中国科技大学':'https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6',
# '清华':'https://www.zhihu.com/search?type=content&q=%E6%B8%85%E5%8D%8E',
# '清华大学':'https://www.zhihu.com/search?type=content&q=%E6%B8%85%E5%8D%8E%E5%A4%A7%E5%AD%A6',
# '北大':'https://www.zhihu.com/search?type=content&q=%E5%8C%97%E5%A4%A7',
# '北京大学':'https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6',
# '复旦':'https://www.zhihu.com/search?type=content&q=%E5%A4%8D%E6%97%A6',
# '复旦大学':'https://www.zhihu.com/search?type=content&q=%E5%A4%8D%E6%97%A6%E5%A4%A7%E5%AD%A6',
# '上交':'https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E4%BA%A4',
# '上海交通大学':'https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E6%B5%B7%E4%BA%A4%E9%80%9A%E5%A4%A7%E5%AD%A6',
# '浙大':'https://www.zhihu.com/search?type=content&q=%E6%B5%99%E5%A4%A7',
# '浙江大学':'https://www.zhihu.com/search?type=content&q=%E6%B5%99%E6%B1%9F%E5%A4%A7%E5%AD%A6',
# '南大':'https://www.zhihu.com/search?type=content&q=%E5%8D%97%E5%A4%A7',
# '南京大学':'https://www.zhihu.com/search?type=content&q=%E5%8D%97%E4%BA%AC%E5%A4%A7%E5%AD%A6'