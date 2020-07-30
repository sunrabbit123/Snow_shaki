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


class ShakiBot(commands.Bot):
    def __init__(self, *, debug = False):
        self.debug = debug
        self.find_func = call_func()
        super().__init__(command_prefix="", help_command=None)

    async def on_ready(self):
        activity = discord.Game(name='"샤키야 도움말" 이라고 해보지 않으련?')
        await self.change_presence(activity=activity)
        print("야생의 샤키가 나타났다!")

   
    @print_time
    async def on_message(self, message):
        await self.wait_until_ready()
        if not message.author.bot and message.content:
            func = self.find_func.func_get(message)

            if func is None:
                
                


            
    


