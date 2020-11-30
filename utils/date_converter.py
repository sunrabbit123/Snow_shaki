import datetime
import discord
import re
from const import Strings
def pattern_Comparison(pattern, text) -> bool:
    comparison = re.search(pattern, text)
    
    if comparison:
        return True
    else:
        return False

def plus_minus_date(date : datetime.datetime, YMWD, value : int) -> datetime.datetime:
    if YMWD == 'Y':
        if value > 0:
            date += datetime.timedelta(days = 365 * value)
        else :
            value *= -1
            date -= datetime.timedelta(days = 365 * value)
    elif YMWD == "M":
        if value > 0:
            date += datetime.timedelta(month = value)
        else :
            value *= -1
            date -= datetime.timedelta(month = value)
    elif YMWD == "W":
        if value > 0:
            date += datetime.timedelta(weeks = value)
        else :
            value *= -1
            date -= datetime.timedelta(weeks = value)
    else :
        if value > 0:
            date += datetime.timedelta(days = value)
        else :
            value *= -1
            date -= datetime.timedelta(days = value)  
    return date

def set_date(text : str, YMWD : str, date : datetime.datetime, val : int = 1) -> datetime.datetime:
    if(pattern_Comparison(re.compile(r'(전|저|지)'), text)):
        date = plus_minus_date(date, YMWD, val * -1)
    else:
        date = plus_minus_date(date, YMWD, val)
    return date
    

def set_Fixed_Date(value : int, YMWD : str, date : datetime.datetime) -> datetime.datetime:
    if YMWD == 'W':
        date = date.replace(day = value * 7)
    elif YMWD == 'D':
        date = date.replace(day = value)
    elif YMWD == 'M':
        date = date.replace(month = value)
    elif YMWD == 'Y':
        date = date.replace(year = value)
    return date

    
class get_date:
    def __init__(self, message : discord.Message ):
        text = ' '.join(message.content.split()[1:])

        Date_Dict = {   "주" : 'W',
                        "달" : 'M',
                        "해" : 'Y',
                        "년" : 'Y'}
        Days_Dict = {   "열흘" : "10",
                        "스무날" : "20",
                        "보름" : "15",
                        "그믐" : "30"}
        self.date = datetime.datetime.now()

        if pattern_Comparison(re.compile(r'\b일 뒤\b|\b월 뒤\b|\b달 뒤\b|\b주 뒤\b'), text) and\
            pattern_Comparison(re.compile('[0-9]'), text):

            YMWD = 'M' if pattern_Comparison(re.compile('[월|달]'), text) else\
                   ('W' if pattern_Comparison(re.compile('[주]'), text) else 'D')
                   
            val = re.sub('[^0-9]', "", text)
            self.date = set_date(text, YMWD, self.date, int(val))

        for days, plus in Strings.dateExp.items():
            if days in text:
                self.date = set_date(text, 'D', self.date, plus)
        
        is_DMY = re.sub('[^주|달|해|년]', "", text)
        is_Days_Dict = re.sub(r'[^\b열흘\b|\b스무날\b|\b보름\b|\b그믐\b]', "", text)
        if is_DMY:
            length = re.sub('[^다|저|지|전]', "", text)
            print(len(length))
            self.date = set_date(text, Date_Dict[is_DMY[0]], self.date, len(length))
        #TODO 지지난주 -> 4주 전으로 체크됨
        elif is_Days_Dict:
            try:
                self.date = set_date(text, 'D', self.date, Days_Dict[is_Days_Dict[0]])
            except Exception as e:
                print(e)


        else:
            for i, j, k in zip(Strings.dateCentury, Strings.dateCenturyAbbr, range(0,9)):
                if pattern_Comparison(re.compile(r'\b{0}\b|\b{1}\b'.format(i, j)), text):

                    if pattern_Comparison(re.compile('[열]'), text):
                        self.date = set_Fixed_Date(k + 11, 'D', self.date)
                    elif pattern_Comparison(re.compile(r'[\b스무\b]'), text):
                        self.date = set_Fixed_Date(k + 21, 'D', self.date)
                    else:
                        self.date = set_Fixed_Date(k + 1, 'D', self.date)

        for week, num in zip(Strings.week, range(0,7)):
            if f"{week}요일" in text:
                self.date = set_Fixed_Date(int(self.date.day) - self.date.weekday() + num, 'D', self.date)
        #TODO 토요일부터는 다음주의 급식을 출력

    def strftime(self):
        week = ['월', '화', '수', '목', '금', '토', '일']
        formatted = self.date.strftime('%Y년 %m월 %d일 ') + week[self.date.weekday()] + "요일"
        return formatted


    def url_date(self):
        formatted = re.sub('[^0-9]', '', str(self.date.__str__()))[2:8]
        return formatted
    
    
        
        
