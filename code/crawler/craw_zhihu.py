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
        # 'pku':['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E5%A4%A7',
        #        'https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6'],
        # 'thu':['https://www.zhihu.com/search?type=content&q=%E6%B8%85%E5%8D%8E',
        #        'https://www.zhihu.com/search?type=content&q=%E6%B8%85%E5%8D%8E%E5%A4%A7%E5%AD%A6'],
        # 'hfut':['https://www.zhihu.com/search?type=content&q=%E5%90%88%E5%B7%A5%E5%A4%A7',
        #         'https://www.zhihu.com/search?type=content&q=%E5%90%88%E8%82%A5%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        # 'ustc':['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E7%A7%91%E5%A4%A7',
        #         'https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6'],
        # 'fudan':['https://www.zhihu.com/search?type=content&q=%E5%A4%8D%E6%97%A6',
        #          'https://www.zhihu.com/search?type=content&q=%E5%A4%8D%E6%97%A6%E5%A4%A7%E5%AD%A6'],
        # 'sjtu':['https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E4%BA%A4',
        #         'https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E6%B5%B7%E4%BA%A4%E9%80%9A%E5%A4%A7%E5%AD%A6'],
        # 'zju':['https://www.zhihu.com/search?type=content&q=%E6%B5%99%E5%A4%A7',
        #        'https://www.zhihu.com/search?type=content&q=%E6%B5%99%E6%B1%9F%E5%A4%A7%E5%AD%A6'],
        # 'nju':['https://www.zhihu.com/search?type=content&q=%E5%8D%97%E5%A4%A7',
        #        'https://www.zhihu.com/search?type=content&q=%E5%8D%97%E4%BA%AC%E5%A4%A7%E5%AD%A6']
        'ruc'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E4%BA%BA%E6%B0%91%E5%A4%A7%E5%AD%A6'],
        'bjtu'      :['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E4%BA%A4%E9%80%9A%E5%A4%A7%E5%AD%A6'],
        'bjut'      :['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        'buaa'      :['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E8%88%AA%E7%A9%BA%E8%88%AA%E5%A4%A9%E5%A4%A7%E5%AD%A6'],
        'bit'       :['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6'],
        'ustb'      :['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6'],
        'buct'      :['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E5%8C%96%E5%B7%A5%E5%A4%A7%E5%AD%A6'],
        'bupt'      :['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E9%82%AE%E7%94%B5%E5%A4%A7%E5%AD%A6'],
        'cau'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E5%86%9C%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        'bjfu'      :['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E6%9E%97%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        'cuc'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E4%BC%A0%E5%AA%92%E5%A4%A7%E5%AD%A6'],
        'muc'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%A4%AE%E6%B0%91%E6%97%8F%E5%A4%A7%E5%AD%A6'],
        'bnu'       :['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6'],
        'ccom'      :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%A4%AE%E9%9F%B3%E4%B9%90%E5%AD%A6%E9%99%A2'],
        'uibe'      :['https://www.zhihu.com/search?type=content&q=%E5%AF%B9%E5%A4%96%E7%BB%8F%E6%B5%8E%E8%B4%B8%E6%98%93%E5%A4%A7%E5%AD%A6'],
        'bucm'      :['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E4%B8%AD%E5%8C%BB%E8%8D%AF%E5%A4%A7%E5%AD%A6'],
        'bfsu'      :['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E5%A4%96%E5%9B%BD%E8%AF%AD%E5%A4%A7%E5%AD%A6'],
        'cugb'      :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E5%9C%B0%E8%B4%A8%E5%A4%A7%E5%AD%A6%EF%BC%88%E5%8C%97%E4%BA%AC%EF%BC%89'],
        'cug'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E5%9C%B0%E8%B4%A8%E5%A4%A7%E5%AD%A6%EF%BC%88%E6%AD%A6%E6%B1%89%EF%BC%89'],
        'cumtb'     :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E7%9F%BF%E4%B8%9A%E5%A4%A7%E5%AD%A6%EF%BC%88%E5%8C%97%E4%BA%AC%EF%BC%89'],
        'cumt'      :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E7%9F%BF%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        'upc'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E7%9F%B3%E6%B2%B9%E5%A4%A7%E5%AD%A6'],
        'cup'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E7%9F%B3%E6%B2%B9%E5%A4%A7%E5%AD%A6%EF%BC%88%E5%8C%97%E4%BA%AC%EF%BC%89'],
        'cupl'      :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E6%94%BF%E6%B3%95%E5%A4%A7%E5%AD%A6'],
        'cufe'      :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%A4%AE%E8%B4%A2%E7%BB%8F%E5%A4%A7%E5%AD%A6'],
        'bsu'       :['https://www.zhihu.com/search?type=content&q=%E5%8C%97%E4%BA%AC%E4%BD%93%E8%82%B2%E5%A4%A7%E5%AD%A6'],
        'sisu'      :['https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E6%B5%B7%E5%A4%96%E5%9B%BD%E8%AF%AD%E5%A4%A7%E5%AD%A6'],
        'ecnu'      :['https://www.zhihu.com/search?type=content&q=%E5%8D%8E%E4%B8%9C%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6'],
        'shu'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E6%B5%B7%E5%A4%A7%E5%AD%A6'],
        'dhu'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%9C%E5%8D%8E%E5%A4%A7%E5%AD%A6'],
        'sufe'      :['https://www.zhihu.com/search?type=content&q=%E4%B8%8A%E6%B5%B7%E8%B4%A2%E7%BB%8F%E5%A4%A7%E5%AD%A6'],
        'ecust'     :['https://www.zhihu.com/search?type=content&q=%E5%8D%8E%E4%B8%9C%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6'],
        'tongji'    :['https://www.zhihu.com/search?type=content&q=%E5%90%8C%E6%B5%8E%E5%A4%A7%E5%AD%A6'],
        'nku'       :['https://www.zhihu.com/search?type=content&q=%E5%8D%97%E5%BC%80%E5%A4%A7%E5%AD%A6'],
        'tju'       :['https://www.zhihu.com/search?type=content&q=%E5%A4%A9%E6%B4%A5%E5%A4%A7%E5%AD%A6'],
        'tjmu'      :['https://www.zhihu.com/search?type=content&q=%E5%A4%A9%E6%B4%A5%E5%8C%BB%E7%A7%91%E5%A4%A7%E5%AD%A6'],
        'hebut'     :['https://www.zhihu.com/search?type=content&q=%E6%B2%B3%E5%8C%97%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        'cqu'       :['https://www.zhihu.com/search?type=content&q=%E9%87%8D%E5%BA%86%E5%A4%A7%E5%AD%A6'],
        'swu'       :['https://www.zhihu.com/search?type=content&q=%E8%A5%BF%E5%8D%97%E5%A4%A7%E5%AD%A6'],
        'ncepu'     :['https://www.zhihu.com/search?type=content&q=%E5%8D%8E%E5%8C%97%E7%94%B5%E5%8A%9B%E5%A4%A7%E5%AD%A6'],
        'tut'       :['https://www.zhihu.com/search?type=content&q=%E5%A4%AA%E5%8E%9F%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6'],
        'imu'       :['https://www.zhihu.com/search?type=content&q=%E5%86%85%E8%92%99%E5%8F%A4%E5%A4%A7%E5%AD%A6'],
        'dut'       :['https://www.zhihu.com/search?type=content&q=%E5%A4%A7%E8%BF%9E%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6'],
        'neu'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%9C%E5%8C%97%E5%A4%A7%E5%AD%A6'],
        'lnu'       :['https://www.zhihu.com/search?type=content&q=%E8%BE%BD%E5%AE%81%E5%A4%A7%E5%AD%A6'],
        'dmu'       :['https://www.zhihu.com/search?type=content&q=%E5%A4%A7%E8%BF%9E%E6%B5%B7%E4%BA%8B%E5%A4%A7%E5%AD%A6'],
        'jlu'       :['https://www.zhihu.com/search?type=content&q=%E5%90%89%E6%9E%97%E5%A4%A7%E5%AD%A6'],
        'nenu'      :['https://www.zhihu.com/search?type=content&q=%E4%B8%9C%E5%8C%97%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6'],
        'ybu'       :['https://www.zhihu.com/search?type=content&q=%E5%BB%B6%E8%BE%B9%E5%A4%A7%E5%AD%A6'],
        'hit'       :['https://www.zhihu.com/search?type=content&q=%E5%93%88%E5%B0%94%E6%BB%A8%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        'heu'       :['https://www.zhihu.com/search?type=content&q=%E5%93%88%E5%B0%94%E6%BB%A8%E5%B7%A5%E7%A8%8B%E5%A4%A7%E5%AD%A6'],
        'neau'      :['https://www.zhihu.com/search?type=content&q=%E4%B8%9C%E5%8C%97%E5%86%9C%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        'nefu'      :['https://www.zhihu.com/search?type=content&q=%E4%B8%9C%E5%8C%97%E6%9E%97%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        'seu'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%9C%E5%8D%97%E5%A4%A7%E5%AD%A6'],
        'suda'      :['https://www.zhihu.com/search?type=content&q=%E8%8B%8F%E5%B7%9E%E5%A4%A7%E5%AD%A6'],
        'njnu'      :['https://www.zhihu.com/search?type=content&q=%E5%8D%97%E4%BA%AC%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6'],
        'cpu'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E8%8D%AF%E7%A7%91%E5%A4%A7%E5%AD%A6'],
        'hhu'       :['https://www.zhihu.com/search?type=content&q=%E6%B2%B3%E6%B5%B7%E5%A4%A7%E5%AD%A6'],
        'njust'     :['https://www.zhihu.com/search?type=content&q=%E5%8D%97%E4%BA%AC%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6'],
        'jiangnan'  :['https://www.zhihu.com/search?type=content&q=%E6%B1%9F%E5%8D%97%E5%A4%A7%E5%AD%A6'],
        'njau'      :['https://www.zhihu.com/search?type=content&q=%E5%8D%97%E4%BA%AC%E5%86%9C%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        'nuaa'      :['https://www.zhihu.com/search?type=content&q=%E5%8D%97%E4%BA%AC%E8%88%AA%E7%A9%BA%E8%88%AA%E5%A4%A9%E5%A4%A7%E5%AD%A6'],
        'xmu'       :['https://www.zhihu.com/search?type=content&q=%E5%8E%A6%E9%97%A8%E5%A4%A7%E5%AD%A6'],
        'fzu'       :['https://www.zhihu.com/search?type=content&q=%E7%A6%8F%E5%B7%9E%E5%A4%A7%E5%AD%A6'],
        'ncu'       :['https://www.zhihu.com/search?type=content&q=%E5%8D%97%E6%98%8C%E5%A4%A7%E5%AD%A6'],
        'sdu'       :['https://www.zhihu.com/search?type=content&q=%E5%B1%B1%E4%B8%9C%E5%A4%A7%E5%AD%A6'],
        'ouc'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%9B%BD%E6%B5%B7%E6%B4%8B%E5%A4%A7%E5%AD%A6'],
        'zzu'       :['https://www.zhihu.com/search?type=content&q=%E9%83%91%E5%B7%9E%E5%A4%A7%E5%AD%A6'],
        'whu'       :['https://www.zhihu.com/search?type=content&q=%E6%AD%A6%E6%B1%89%E5%A4%A7%E5%AD%A6'],
        'hust'      :['https://www.zhihu.com/search?type=content&q=%E5%8D%8E%E4%B8%AD%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6'],
        'wut'       :['https://www.zhihu.com/search?type=content&q=%E6%AD%A6%E6%B1%89%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6'],
        'zuel'      :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%8D%97%E8%B4%A2%E7%BB%8F%E6%94%BF%E6%B3%95%E5%A4%A7%E5%AD%A6'],
        'ccnu'      :['https://www.zhihu.com/search?type=content&q=%E5%8D%8E%E4%B8%AD%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6'],
        'hzau'      :['https://www.zhihu.com/search?type=content&q=%E5%8D%8E%E4%B8%AD%E5%86%9C%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        'hnu'       :['https://www.zhihu.com/search?type=content&q=%E6%B9%96%E5%8D%97%E5%A4%A7%E5%AD%A6'],
        'csu'       :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%8D%97%E5%A4%A7%E5%AD%A6'],
        'hunnu'     :['https://www.zhihu.com/search?type=content&q=%E6%B9%96%E5%8D%97%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6'],
        'sysu'      :['https://www.zhihu.com/search?type=content&q=%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A6'],
        'jnu'       :['https://www.zhihu.com/search?type=content&q=%E6%9A%A8%E5%8D%97%E5%A4%A7%E5%AD%A6'],
        'scut'      :['https://www.zhihu.com/search?type=content&q=%E5%8D%8E%E5%8D%97%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6'],
        'scnu'      :['https://www.zhihu.com/search?type=content&q=%E5%8D%8E%E5%8D%97%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6'],
        'gxu'       :['https://www.zhihu.com/search?type=content&q=%E5%B9%BF%E8%A5%BF%E5%A4%A7%E5%AD%A6'],
        'scu'       :['https://www.zhihu.com/search?type=content&q=%E5%9B%9B%E5%B7%9D%E5%A4%A7%E5%AD%A6'],
        'swjtu'     :['https://www.zhihu.com/search?type=content&q=%E8%A5%BF%E5%8D%97%E4%BA%A4%E9%80%9A%E5%A4%A7%E5%AD%A6'],
        'uestc'     :['https://www.zhihu.com/search?type=content&q=%E7%94%B5%E5%AD%90%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6'],
        'sau'       :['https://www.zhihu.com/search?type=content&q=%E5%9B%9B%E5%B7%9D%E5%86%9C%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        'swufe'     :['https://www.zhihu.com/search?type=content&q=%E8%A5%BF%E5%8D%97%E8%B4%A2%E7%BB%8F%E5%A4%A7%E5%AD%A6'],
        'ynu'       :['https://www.zhihu.com/search?type=content&q=%E4%BA%91%E5%8D%97%E5%A4%A7%E5%AD%A6'],
        'gzu'       :['https://www.zhihu.com/search?type=content&q=%E8%B4%B5%E5%B7%9E%E5%A4%A7%E5%AD%A6'],
        'nwu'       :['https://www.zhihu.com/search?type=content&q=%E8%A5%BF%E5%8C%97%E5%A4%A7%E5%AD%A6'],
        'xjtu'      :['https://www.zhihu.com/search?type=content&q=%E8%A5%BF%E5%AE%89%E4%BA%A4%E9%80%9A%E5%A4%A7%E5%AD%A6'],
        'nwpu'      :['https://www.zhihu.com/search?type=content&q=%E8%A5%BF%E5%8C%97%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6'],
        'chd'       :['https://www.zhihu.com/search?type=content&q=%E9%95%BF%E5%AE%89%E5%A4%A7%E5%AD%A6'],
        'nwafu'     :['https://www.zhihu.com/search?type=content&q=%E8%A5%BF%E5%8C%97%E5%86%9C%E6%9E%97%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6'],
        'snnu'      :['https://www.zhihu.com/search?type=content&q=%E9%99%95%E8%A5%BF%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6'],
        'xidian'    :['https://www.zhihu.com/search?type=content&q=%E8%A5%BF%E5%AE%89%E7%94%B5%E5%AD%90%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6'],
        'lzu'       :['https://www.zhihu.com/search?type=content&q=%E5%85%B0%E5%B7%9E%E5%A4%A7%E5%AD%A6'],
        'hainan'    :['https://www.zhihu.com/search?type=content&q=%E6%B5%B7%E5%8D%97%E5%A4%A7%E5%AD%A6'],
        'nxu'       :['https://www.zhihu.com/search?type=content&q=%E5%AE%81%E5%A4%8F%E5%A4%A7%E5%AD%A6'],
        'qhu'       :['https://www.zhihu.com/search?type=content&q=%E9%9D%92%E6%B5%B7%E5%A4%A7%E5%AD%A6'],
        'tu'        :['https://www.zhihu.com/search?type=content&q=%E8%A5%BF%E8%97%8F%E5%A4%A7%E5%AD%A6'],
        'xju'       :['https://www.zhihu.com/search?type=content&q=%E6%96%B0%E7%96%86%E5%A4%A7%E5%AD%A6'],
        'smmu'      :['https://www.zhihu.com/search?type=content&q=%E7%AC%AC%E4%BA%8C%E5%86%9B%E5%8C%BB%E5%A4%A7%E5%AD%A6'],
        'nudt'      :['https://www.zhihu.com/search?type=content&q=%E5%9B%BD%E9%98%B2%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6'],
        'fmmu'      :['https://www.zhihu.com/search?type=content&q=%E7%AC%AC%E5%9B%9B%E5%86%9B%E5%8C%BB%E5%A4%A7%E5%AD%A6']
        # 在这里添加其他学校的缩写与相关关键词的链接    
    }
    
    zh = ZhiHu()
    for school, urls in school_urls.items():
        zh.access(school, urls)
        time.sleep(3)



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