# region import
import discord
from discord.ext import commands

import random
import asyncio

import pymongo

from const import Strings, Docs, CommandType
from funcs import *
from model import CustomCommandModel as CCM

# endregion

# region util
def command_find(message, prefixed=True):
    diction = getattr(Strings, "command_prefixes" if prefixed else "commands")
    for command, string in diction.items():
        if message in string:
            return command


async def change_again_presence(bot_object: commands.bot, activity_list):
    url = Docs.url
    while not bot_object.is_closed():
        for g in activity_list:
            await bot_object.change_presence(
                status=discord.Status.online,
                activity=discord.Streaming(name=g, url=url),
            )
            await asyncio.sleep(5)
        activity_list[-1] = f"{len(bot_object.guilds)}개의 서버에 참가중입니다!"


command_type = {
    "custom": CustomCommand,
    "school": SchoolCommand,
    "basic": BasicCommand,
}

# endregion


class ShakiBot(commands.Bot):
    def __init__(
        self,
        db: pymongo.database.Database,
        *,
        debug=False,
        admin: str = "508788780002443284",
    ):
        self.debug = debug
        # self.dbmanger = dbmanger()
        self.prefix = Strings.bot_prefix
        self.prefixed = 0
        self.admin = admin
        self.db = db
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
        await self.wait_until_ready()  # 준비가 될때까지 대기
        if message.author.bot:
            return
            # 봇이 아닐때만 작동
        # 소문자로 바꾸고, 공백기준으로 나눠줌
        messages = message.content.lower().split()

        try:
            prefixed = 1 if (messages[0] in self.prefix) else 0
            # 문장 맨 처음이 프리픽스가 들어가있다면 1, 아니라면 0
        except IndexError:
            return
        # 사진이면 리턴

        try:
            command = messages[prefixed]
            # 명령어는 프리픽스가 있으면 두번째, 없다면 첫번째
        except IndexError:
            await message.channel.send("먀아,,,?")
            # 못알아먹으면 먀아?

        finded_command = None  # 선언
        try:
            finded_command = command_find(command, prefixed=prefixed) or (
                command_find(messages[2], prefixed=True)
                or command_find(messages[-1], prefixed=True)
                if prefixed
                else None
            )
        except IndexError:
            pass  # messages[2]를 조회함으로써 생기는 에러
        # 커맨드 조회
        func = None  # 변수선언
        if finded_command:
            try:
                type_of_command_flag = getattr(CommandType, finded_command)
                extension = command_type[type_of_command_flag]
                func = getattr(extension, f"command_{finded_command}")

                print(
                    "%s : %s : %s"
                    % (message.author, message.channel.name, message.content)
                )
            except (UnicodeEncodeError, AttributeError):
                pass  # 유니코드 에러는 스킵, 해당 클래스에 해당 함수가 없어도 스킵

            if func:
                if type_of_command_flag == "basic":  # 나머지는 db 필요
                    await func(message)
                elif finded_command == "regist":
                    await func(message, self.db, self)
                else:
                    await func(message, self.db)
        elif prefixed:
            try:
                value_command = random.choice(CCM(self.db).command_select(message))
                await message.channel.send(value_command["value-command"])
            except IndexError:
                pass  # 값이 없을 경우 choice가 불가능하기에 IndexError이 나타남
