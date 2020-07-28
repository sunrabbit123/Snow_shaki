import asyncio
from openpyxl import load_workbook

import random

class study_pathfind:
    
    def command_C(self, message):
        link = "www.inflearn.com/course/c%EC%96%B8%EC%96%B4-%EB%91%90%EB%93%A4%EB%82%99%EC%84%9C"
        return link

    def command_python(self, message):
        link = "wikidocs.net/book/1"
        return link

    def command_javascript(self,message): 
        print("호출은 됨")

        return str('opentutorials.org/course/743')

    def command_html(self, message):
        link = ["opentutorials.org/course/2039","opentutorials.org/course/2418"]
        return random.choice(link)


    

