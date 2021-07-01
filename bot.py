# region import
import discord
from discord.ext import commands

import random
import asyncio

from const import Strings, Docs
from funcs import basic_command, custom_command
from model import custom_command as custom_db

# endregion

# region util
def command_find(message, prefixed=True):
    diction = getattr(Strings, "command_prefixes" if prefixed else "commands")
    for command, string in diction.items():
        if message in string:
            return command


async def change_again_presence(bot_object : commands.bot, activity_list):
    url = Docs.url
    while not bot_object.is_closed():
        for g in activity_list:
            await bot_object.change_presence(
                status=discord.Status.online, activity=discord.Streaming(name=g, url=url)
            )
            await asyncio.sleep(5)
        activity_list[-1] = f"{len(bot_object.guilds)}개의 서버에 참가중입니다!"


# endregion


class ShakiBot(commands.Bot):
    def __init__(self, db, *, debug=False, admin: str = "508788780002443284"):
        self.debug = debug
        # self.dbmanger = dbmanger()
        self.prefix = Strings.bot_prefix
        self.prefixed = 0
        self.admin = admin
        self.db = custom_db(db)
        super().__init__(command_prefix=None, help_command=None)

    async def on_ready(self):

        guild_list = [guild.name for guild in self.guilds]
        print(guild_list)
        print("야생의 샤키가 나타났다!")
        activity_list = Strings.activity_list
        activity_list.append(f"{len(guild_list)}개의 서버에 참가중입니다!")
        await self.wait_until_ready()
        await change_again_presence(self, activity_list)

    async def on_message(self, message: discord.Message):
        await self.wait_until_ready()
        if message.author.bot:
            return
            # 봇이 아닐때만 작동

        command = message.content.lower().split()

        try:
            prefixed = 1 if (command[0] in self.prefix) else 0
        except IndexError:
            return
        # 사진이면 리턴

        try:
            command = command[prefixed]
        except IndexError:
            await message.channel.send("먀아,,,?")

        finded_command = command_find(command, prefixed=prefixed)
        command_type = finded_command not in Strings.custom
        # True == basic_command
        # False == custom_command
        extension = basic_command if command_type else custom_command

        func = None
        try:
            func = getattr(extension, f"command_{finded_command}")

            print(
                "%s : %s : %s"
                % (message.author, message.channel.name, message.content)
            )
        except (UnicodeEncodeError, AttributeError):
            pass  # 유니코드 에러는 스킵, 해당 클래스에 해당 함수가 없어도 스킵

        if not func and message.content[0] == ".":
            meal_word_list = getattr(Strings, "meal")
            meal_sign = message.content.split()[0][1:]
            if meal_sign in meal_word_list:
                func = getattr(extension, "command_급식")
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
                    pass  # 값이 없을 경우 choice가 불가능하기에 IndexError이 나타남
                return