#encoding: utf-8

import requests
import sys
import re
from bs4 import BeautifulSoup

class SpiderBase(object):

    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"}


class HuangliSpider(SpiderBase):


    api_url = "https://nongli.911cha.com/"
    def get_current_calender(self):
        html = requests.get(self.api_url,headers=self.headers).text
        re_pattern = "今日.*?年柱.*?<br />(.*?)</td>.*?月柱.*?<br />(.*?)</td>.*?日柱.*?<br />(.*?)</td>.*?时柱.*?<br />(.*?)</td>"
        r = re.search(re_pattern,html)
        return r.group(1),r.group(2),r.group(3),r.group(4)



if __name__ == '__main__':
    a = HuangliSpider()
    print(a.get_current_calender())
