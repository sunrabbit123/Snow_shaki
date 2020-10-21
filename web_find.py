import aiohttp
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

import datetime
import random

import json
import asyncio
import re

from utils import get_date


class HTMLGetter:
    def __init__(self, url):
        self.url = url

    async def get_html(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        async with aiohttp.ClientSession() as cs:
            html = await cs.get(self.url, headers = headers)
            return await html.text()
        
    async def get_soup(self):
        html = await self.get_html()
        try:
            return BeautifulSoup(html,'html.parser')
        except Exception as e:
            print("error")
            print(e)
         

class SearchWord:
    async def get_dic(self, keyword):
        
        soup = await HTMLGetter("https://terms.naver.com/search.nhn?query=%s&searchType=&dicType=&subject="%keyword).get_soup()
        
        try :
            expl = soup.find('div' , class_ = "info_area").text
            return expl
        except Exception as e:
            print("검색불가")
            print(e)
            return None

    async def get_image(self, keyword):
        soup = await HTMLGetter(f"https://www.google.co.kr/search?q={keyword}&source=lnms&tbm=isch").get_soup()
        # https://www.google.co.kr/search?q=%EB%9D%BC%EC%9D%B4%EC%B8%84
        try :
            info = soup.find_all("img")
            index = random.randint(1, len(info))
            return info[index]["data-src"]
        except Exception as e:
            print(e)
            return None

    @staticmethod
    async def get_meal(date : str):
        # region URL
        URL = "https://open.neis.go.kr/hub/mealServiceDietInfo?"\
            + "Type=json"\
			+ "&KEY=bfa95730b1b84b07b2db733b2138d9aa"\
            + "&pIndex=1"\
            + "&pSize=100"\
			+ "&ATPT_OFCDC_SC_CODE=F10"\
			+ "&SD_SCHUL_CODE=7380292"
        URL += "&MLSV_YMD=" + date
        # endregion
        print(URL)
        data = json.loads(await HTMLGetter(URL).get_html())
        return data
        


if __name__ == "__main__":
    pass

            
        
        
