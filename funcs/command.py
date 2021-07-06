import discord

import random
import re
import os

from utils import set_embed, SearchWord
from const import Docs, Strings


class BasicCommand:
    @staticmethod
    async def command_help(message: discord.Message):
        em = set_embed(message, title="샤키의 도움말 목록")
        for i in range(len(Docs.help_title)):
            em.add_field(
                name=Docs.help_title[i], value=Docs.help_description[i], inline=False
            )
        em.set_footer(text=Docs.NH)
        await message.channel.send(embed=em)

    @staticmethod
    async def command_clean_messages(message: discord.Message):
        contents = message.content.split()
        messages_to_delete = 10

        if len(contents) > 2:
            try:
                messages_to_delete = int(contents[-1])
            except (ValueError):
                await message.channel.send("숫자를 입력해주세요")
                return

        deleted = await message.channel.purge(
            limit=messages_to_delete + 1, check=lambda m: m.id != message.id
        )
        await message.channel.send(f"{len(deleted)}개의 메세지를 지웠어요!")

    @staticmethod
    async def command_emoji(message: discord.Message):
        await message.channel.send(random.choice(Strings.emoji))

    @staticmethod
    async def command_choice(message: discord.Message):
        chlist = message.content.split()[2:]
        await message.channel.send(f"내가 뽑은건...!\n{random.choice(chlist)}입니당!")

    @staticmethod
    async def command_굴러(message: discord.Message):
        await message.channel.send(Strings.roll)

    @staticmethod
    async def command_구글검색(message: discord.Message):
        findg = " ".join(message.content.split()[2:])
        image = await SearchWord().get_image(findg)
        em = None
        if image is None:
            await message.channel.send("이미지 불러오기를 실패했습니다")
            return
        else:
            em = set_embed(message, title=f"{findg}의 이미지 검색 결과")
            em.set_image(url=image)
        await message.channel.send(embed=em)

    @staticmethod
    async def command_사전검색(message: discord.Message):
        findn = " ".join(message.content.split()[2:])
        findit = await SearchWord().get_dic(findn)

        if findit is None:
            await message.channel.send("사전검색이 실패했습니다.")

        else:
            em = set_embed(message, title=f"{findn}의 네이버 사전검색 결과", description=findit)
            await message.channel.send(embed=em)

    @staticmethod
    async def command_링크(message: discord.Message):
        await message.channel.send(
            discord.utils.oauth_url(
                client_id=os.environ["client"],
                permissions=discord.Permissions(permissions=1610837057),
            )
        )
        await message.channel.send("여기 있어요,,,")
