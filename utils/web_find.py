from .url_manager import url_manager
import aiohttp
from bs4 import BeautifulSoup
import random
import json
import asyncio


class HTMLGetter:
    def __init__(self, url):
        self.url = url

    async def get_html(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        async with aiohttp.ClientSession() as cs:
            html = await cs.get(self.url, headers=headers)
            return await html.text()

    async def get_json(self):
        html = await self.get_html()
        data = BeautifulSoup(html, "html.parser")
        jsonData = json.loads(data.get_text())
        return jsonData

    async def get_soup(self):
        html = await self.get_html()
        try:
            return BeautifulSoup(html, "html.parser")
        except Exception as e:
            print("error")
            print(e)


class SearchWord:
    @staticmethod
    async def get_dic(keyword: str):

        soup = await HTMLGetter(
            "https://terms.naver.com/search.nhn?query=%s&searchType=&dicType=&subject="
            % keyword
        ).get_soup()

        try:
            expl = soup.find("div", class_="info_area").text
            return expl
        except Exception as e:
            print("검색불가")
            print(e)
            return None

    @staticmethod
    async def get_image(keyword: str):
        soup = await HTMLGetter(
            f"https://www.google.co.kr/search?q={keyword}&source=lnms&tbm=isch"
        ).get_soup()
        # https://www.google.co.kr/search?q=%EB%9D%BC%EC%9D%B4%EC%B8%84
        try:
            info = soup.find_all("img")
            index = random.randint(1, len(info))
            link = str(info[index]).split("src=")[1].split('"')[1]
            return link
        except Exception as e:
            print("err :", e)
            return None


class NeisAPI:
    auth_key = "bfa95730b1b84b07b2db733b2138d9aa"

    @staticmethod
    async def get_meal(date: str, ATPT_OFCDC_SC_CODE: str, SCHOOL_CODE: str):
        # region URL
        addition = [
            f"MLSV_YMD={date}",
            f"ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}",
            f"SD_SCHUL_CODE={SCHOOL_CODE}",
        ]
        url: str = url_manager(
            type="mealServiceDietInfo", additions=addition, auth_key=NeisAPI.auth_key
        ).get_url()
        # endregion
        print(url)
        return await HTMLGetter(url).get_json()

    @staticmethod
    async def search_school(school: str):
        url: str = url_manager(
            type="schoolInfo",
            additions=[f"SCHUL_NM={school}"],
            auth_key=NeisAPI.auth_key,
        ).get_url()
        return await HTMLGetter(url).get_json()

    @staticmethod
    async def get_schedule(**school_info):
        school_type: dict = {
            "초등학교": "elsTimetable",
            "중학교": "misTimetable",
            "고등학교": "hisTimetable",
            "특수학교": "spsTimetable",
        }

        addition: list = [
            "ATPT_OFCDC_SC_CODE=%s" % school_info["ATPT_OFCDC_SC_CODE"],  # 교육청
            "SD_SCHUL_CODE=%s" % school_info["SCHOOL_INFO"],  # 학교
            "ALL_TI_YMD=%s" % school_info["ALL_TI_YMD"],  # 일자
            "GRADE=%s" % school_info["GRADE"],  # 학년
            "CLASS_NM=%s" % school_info["CLASS_NM"],  # 반
        ]

        url: str = url_manager(
            type=school_type[school_info["SCHUL_KND_SC_NM"]],
            additions=addition,
            auth_key=NeisAPI.auth_key,
        ).get_url()
        print(url)
        return await HTMLGetter(url).get_json()
