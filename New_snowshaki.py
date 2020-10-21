# region import
import discord
from discord.ext import commands

import asyncio
import random
import time
import datetime
from functools import partial

import operator
import os
import re

import pymongo
from const import Docs, Strings
from web_find import SearchWord
from funcs import basic_command, custom_command
from model import custom_command as custom_db
from utils import print_time, set_embed

# endregion

# region command
def command_find(message, prefixed = True):
    diction = getattr(Strings,'command_prefixes' if prefixed else 'commands')
    for command, string in diction.items():
        if message in string:
            return command
# endregion



class ShakiBot(commands.Bot):
    def __init__(self, db, *, debug = False, admin : str = '508788780002443284'):
        self.debug = debug
        #self.dbmanger = dbmanger()
        self.prefix =["샤키야","참수진","수진아","Shaki","shaki"]
        self.prefixed = 0
        self.admin = admin
        self.db = custom_db(db)

        


        super().__init__(command_prefix = None, help_command=None)

    async def on_ready(self):       
        # activity = discord.Activity(name='"샤키야 도움말" 이라고 해보지 않으련?', type=discord.ActivityType.playing)
        activity = discord.Activity(name='디버깅,,,,', type=discord.ActivityType.playing)

        await self.change_presence(activity=activity)
        print("야생의 샤키가 나타났다!")

   
    async def on_message(self, message : discord.Message):
        await self.wait_until_ready()
        if not message.author.bot:
            # 봇이 아닐때만 작동
            command = message.content.lower().split()

            try:    
                prefixed = 1 if (command[0] in self.prefix) else  0
            except IndexError:
                return
            # 사진이면 리턴

            try:
                command = command[prefixed]
            except IndexError:
                await message.channel.send("먀아,,,?")

            
            finded_command = command_find(command, prefixed = prefixed)
            command_type = finded_command not in Strings.custom
            # True == basic_command
            # False == custom_command
            extension = basic_command if command_type else custom_command
            
            func = None
            try:
                func = getattr(extension, f"command_{finded_command}")
                
                print("%s : %s : %s" % (message.author, message.channel.name, message.content ))
            except (UnicodeEncodeError, AttributeError):
                pass#유니코드 에러는 스킵, 해당 클래스에 해당 함수가 없어도 스킵

            if not func and prefixed:
                diction = getattr(Strings, 'meal')
                for _command, string in diction.items():
                    for meal_command in string:
                        if meal_command in message.content:
                            func = getattr(extension, 'command_급식')
                            await func(message)
                            return
            if func:
                if command_type:
                    await func(message)
                else:
                    await func(message, self.db)
            else:
                if prefixed == False:
                    return
                else:
                    try:
                        value_command = random.choice(self.db.command_select(message))
                        await message.channel.send(value_command["value-command"])
                    except IndexError:
                        pass # 값이 없을 경우 choice가 불가능하기에 IndexError이 나타남
                    return
    

