import discord
from discord.ext import commands

import asyncio
import random
import time
import datetime
import operator
import os
import re
from functools import partial 
from datetime import datetime

from expand import call_func
import base_func
from db_manger import dbmanger





def print_time(func):
    async def wrapper(self, message : discord.message):
        print(datetime.now(), end = ' ')
        return await func(self, message)
    return wrapper

def bad_shaki(func):
    async def wrapper(self, message):
        if message.content.split()[-1] == "굶어":
            await message.channel.send("야랄마세요;; 너나 하세요")
        return await func(self, message)
    return wrapper


class ShakiBot(commands.Bot):
    def __init__(self, *, debug = False):
        self.debug = debug

        super().__init__(command_prefix="", help_command=None)

    async def on_ready(self):
        activity = discord.Game(name='"샤키야 도움말" 이라고 해보지 않으련?')
        await self.change_presence(activity=activity)
        print("야생의 샤키가 나타났다!")

   
    #@print_time
    async def on_message(self, message : discord.message):
        await self.wait_until_ready()
        if not message.author.bot and message.content:
            command_keyword = call_func().func_find(message)
            base_func.command_굴러(self, message)

            if command_keyword is None:#본래 함수에 없다면 사용자지정함수를 확인한다.
                
                searched_data = dbmanger().search_data('made_command', 'keycommand', message.content)
                print(searched_data)
                if searched_data == None:
                    return
                try:
                    server = str(message.guild.id)
                    server_command = [cmd for cmd in searched_data if cmd.server_id == server]
                    searched_msg = random.choice(server_command)
                    await message.chnnel.send(searched_msg.output) 
                except (IndexError, ValueError):
                    return
            else:
                func = "base_func." + command_keyword + "(self, message)"
                print(func)
                await exec(func)
                


            
    


