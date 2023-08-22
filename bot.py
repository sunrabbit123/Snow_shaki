# region import
import discord
from discord.ext import commands

import random
import asyncio

import pymongo

from const import Strings, CommandType
from funcs import *
from model import CustomCommandModel as CCM

# endregion


# region util
def command_find(message, prefixed=True) -> any | None:
    diction = getattr(Strings, "command_prefixes" if prefixed else "commands")
    for command, string in diction.items():
        if message in string:
            return command


def get_command(messages: [str], prefixed: bool) -> any | None:
    if len(messages) < 2:
        return None

    command = command_find(messages[1 if prefixed else 0], prefixed=prefixed)
    if command:
        return command

    if not prefixed:
        return None

    try:
        return command_find(messages[2], prefixed=True) or command_find(
            messages[-1], prefixed=True
        )
    except IndexError:
        return None
        # messages[2]를 조회함으로써 생기는 에러


def get_method(command: str) -> any | None:
    try:
        type_of_command_flag = getattr(CommandType, command)
        extension = command_type[type_of_command_flag]
        func = getattr(extension, f"command_{command}")
        return [type_of_command_flag, func]
    except (UnicodeEncodeError, AttributeError):
        pass  # 유니코드 에러는 스킵, 해당 클래스에 해당 함수가 없어도 스킵


async def change_again_presence(bot_object: commands.bot, activity_list):
    url = discord.utils.oauth_url(
        client_id=700605291196186634,
        permissions=discord.Permissions(permissions=1610837057),
    )
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
        super().__init__(
            command_prefix=None, help_command=None, intents=discord.Intents.all()
        )

    async def on_ready(self):
        guild_list = [guild.name for guild in self.guilds]
        print(f"List of linked {len(guild_list)} servers : {guild_list}")
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

        message_length = len(messages)

        if message_length is 0:
            return

        if message_length is 1:
            if messages[0] != "." and messages[0] != "ㅅ":
                await message.channel.send("먀아,,,?")
            return

        prefixed = messages[0] in self.prefix

        command = get_command(messages, prefixed)
        # 커맨드 조회
        if command:
            res = get_method()

            command_flag = res[0]
            func = res[1]

            if func is None:
                return
            print(
                "%s : %s : %s" % (message.author, message.channel.name, message.content)
            )
            if command_flag == "basic":  # 나머지는 db 필요
                await func(message)
                return

            if command != "regist":
                await func(message, self.db)
                return

            await func(message, self.db, self)
            return

        if not prefixed:
            return

        try:
            value_command = random.choice(CCM(self.db).command_select(message))
            await message.channel.send(value_command["value-command"])
        except IndexError:
            pass  # 값이 없을 경우 choice가 불가능하기에 IndexError이 나타남
