from openpyxl import load_workbook
import discord
import asyncio
import random
import time
import datetime

import operator
import os
import re

from functools import partial
from datetime import datetime
from const import Docs,Strings
from web_find import SearchWord
from custom_manger import command_manger
#from db_manger import  dbmanger
from const import study_pathfind


def command_find(message,prefixed = True):
    diction = getattr(Strings,'command_prefixes' if prefixed else 'commands')
    for command, string in diction.items():
        if message in string:
            return command


def print_time(func):
    async def wrapper(self, message):
        print(datetime.now(), end = ' ')
        return await func(self, message)
    return wrapper

def bad_shaki(func):
    async def wrapper(self, message):
        if message.content.split()[-1] == "굶어":
            await message.channel.send("야랄마세요;; 너나 하세요")
        return await func(self, message)
    return wrapper


class ShakiBot(discord.Client):
    def __init__(self,*,debug = False):
        self.debug = debug
        #self.dbmanger = dbmanger()
        self.color = 0x7ACDF4
        self.prefix =["샤키야","참수진","수진아","Shaki","shaki"]
        self.prefixed = 0
        


        super().__init__()

    async def on_ready(self):
        activity = discord.Activity(name='"샤키야 도움말" 이라고 해보지 않으련?', type=discord.ActivityType.playing)
        await self.change_presence(activity=activity)
        print("야생의 샤키가 나타났다!")

   
    @print_time
    async def on_message(self, message):
        await self.wait_until_ready()
        if not message.author.bot:
            command = message.content.lower().split()
            try:    
                prefixed = 1 if (command[0] in self.prefix) else  0
                command = command[prefixed]
            except IndexError:
                return
            
            func = getattr(self, "command_%s"%command_find(command, prefixed=prefixed),None)

            try:
                print("%s : %s : %s" % (message.author,message.channel.name,message.content ))
            except UnicodeEncodeError:
                pass#유니코드 에러는 스킵
            if func:
                await func(message)
            else:
                if prefixed == False:
                    # if message.content == "아니":
                    #     await message.channel.send("도대체")
                    # elif message.content == "도대체":
                    #     await message.channel.send("아니")

                    # await self.command_custom_send(message)
                    
                    return
                else:
                    with open("snow_shaki_bot.txt","r",encoding='utf-8') as f:
                        commands = list()
                        saying = message.content[2:]
                        
                        lines = f.readlines()
                        print(lines)
                        for line in lines:
                            line_key = line.split(':;')[0]
                            if line_key in saying:
                                commands.append(line.split(':;')[1])

                        if len(commands) >= 1:
                            send_msg = random.choice(commands)
                            await message.channel.send(send_msg)
                            del commands
                            return
                        else:
                            print("%s는 명령어가 아닙니다.(User : %s)\n" %(command,message.content))
                            return
                
    async def command_help(self,message):
        emb = discord.Embed(title='깔롤랭은 국룰입니다',description=Docs.help,colour=self.color)
        await message.channel.send(embed = emb)

    async def command_choice(self,message):
        chlist = message.content.split()
        chlist = chlist[2:]
        await message.channel.send("내가 뽑은건...!\n%s입니당!"%random.choice(chlist))

    # async def command_study(self, message):
    #     messages = message.content.split()[2]
    #     outputs = study_pathfind().find_study(messages)
    #     await message.channel.send("https://" +outputs)
    #     print(outputs)

        
        
        

    # async def command_custom(self,message,prefixed = True):
    #     await command_manger(message,prefixed)
        


    # async def command_custom_send(self,message,prefixed = False):
    #     contents = message.content.split()
    #     search_msg = self.dbmanger.search_data('made_command','keycommand',contents[0])
        
    #     try:
    #         server = str(message.guild.id)
    #         server_command = [cmd for cmd in search_msg if cmd.server_id == server]
    #         searched_msg = random.choice(server_command)
    #         await message.chnnel.send(searched_msg.output) 
    #     except (IndexError, ValueError):
    #         return
    
    
        
    
    async def command_잊어(self,message):#샤키야 key커맨드
        forget_word = message.content[6:]
        with open('snow_shaki_bot.txt','w', encoding='utf-8') as save_word:
            with open('snow_shaki_bot.txt','r', encoding='utf-8') as read_word:
                lines = read_word.readlines()
                for i in range(len(lines)):
                    if lines[i] in forget_word:
                        try:
                            lines = lines[:i] + lines[i+1:]
                        except IndexError:
                            pass
                save_word.writelines(lines)
        


        await message.channel.send("?\n형신이세요? 알려주고 잊으라하네ㅔ,,,")
        return
        
    

        

    async def command_배워(self,message) :#샤키야 key커맨드 value커맨드
        word = message.content[7:].split(":")
        with open('snow_shaki_bot.txt', 'a', encoding= 'utf-8') as ff:
            ff.write('%s:;%s\n' % (word[0], word[1]))
        
        await message.channel.send("야랄 왜 나한테...")

    
    async def command_구글검색(self,message):
        findg = message.content[9:]
        await message.channel.trigger_typing()
        image = SearchWord().get_image(findg)

        if image is None:
            await message.channel.send("이미지 불러오기를 실패했습니다")

        else:
            em = discord.Embed(title = "%s의 이미지 검색결과" %findg,colour = self.color)
            em.set_image(url = image)
        await message.channel.send(embed = em)
        
        
            
    async def command_사전검색(self,message):
        findn = message.content[9:]
        findit = SearchWord().get_dic(findn)

        if findit is None:
            await message.channel.send("사전검색이 실패했습니다.")

        else:
            em2 = discord.Embed(title = "%s의 네이버사전검색 결과" % findn,description = "%s" %findit,colour = self.color)
            await message.channel.send(embed = em2)
    
    async def command_굴러(self,message):
        await message.channel.send(random.choice(["데구르르 꽝","꽝 데구르르","데구르르 뎅강","ㄷㄱㄹㄹ ㄷㄱ","야랄,,, 너나 구르세요"]))
    
    async def command_Hello(self,message):
        if message.content.split()[0] == "참수진":
            await message.channel.send("뒤져")
        else:
            pass
    # @bad_shaki
    # async def command_급식(self,message):
    #     keyword = message.content.split()[-1]
    #     today_meal = SearchWord().get_meal(keyword = "내일" if keyword == "내일" else "[오늘]" )

        
        
        
    #     morning = today_meal.index("[중식]")
    #     if "[석식]" in today_meal:
    #         afternoon = today_meal.index("[석식]")
        
    #     today_morning = '-\n'.join(today_meal[1:morning])
    #     if "[석식]" in today_meal:
    #         today_afternoon = '-\n'.join(today_meal[morning +1 :afternoon])
    #         today_dinner = '-\n'.join(today_meal[afternoon +1 :])

    #     else:
    #         today_afternoon = '-\n'.join(today_meal[morning+1:])
            
        
        
    #     emb = discord.Embed(title = "**%s의 급식 **" % ("[내일]" if keyword == "내일" else "[오늘]"), colour = self.color)
       
    #     emb.add_field(name = "[조식]", value = today_morning,inline = False)
    #     emb.add_field(name = "[중식]", value = today_afternoon, inline = False)
    #     if "[석식]" in today_meal:
    #         emb.add_field(name = "[석식]", value = today_dinner, inline = False)

    #     await message.channel.send(embed = emb)


