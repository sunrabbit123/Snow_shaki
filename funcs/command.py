import discord

import random
import os
import re

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
        await message.channel.purge(limit=5, check=lambda m: m.id == message.id)

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
        searcher = SearchWord()
        async def get_image(i):
            print(f"{i}번째 이미지 검색 중")
            return await searcher.get_image(findg)
        em = None
        img = await get_image(1)
        
        for i in range(10):
            if img is not None and img.startswith("http"):
                em = set_embed(message, title=f"{findg}의 이미지 검색 결과")
                em.set_image(url=img)
                await message.channel.send(embed=em)
                return
            img = await get_image(i + 2)     
        await message.channel.send("이미지 불러오기를 실패했습니다")
            

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

    @staticmethod
    async def command_vote(message: discord.Message):
        removed_prefix_message = message.content.split()[2:]

        if len(removed_prefix_message) == 0:
            em: discord.Embed = set_embed(message, title="투표 도움말", has_footer=False)
            em.add_field(name="찬반 투표", value='샤키야 투표 "제목"', inline=False)
            em.add_field(
                name="항목 투표", value='샤키야 투표 "제목" "내용1" "내용2" ...', inline=False
            )
            em.set_footer(text='투표 생성 시 각 항목들은 " "(따옴표)를 통해 구별해야합니다.')
            await message.channel.send(embed=em)
            return

        vote_item_list = re.findall(r'"(.*?)"', " ".join(removed_prefix_message))
        item_length = len(vote_item_list)

        if item_length == 1:
            voted = await message.channel.send(f"**{vote_item_list[0]}**")
            await voted.add_reaction(Strings.thumbs(True))
            await voted.add_reaction(Strings.thumbs(False))
            return

        if item_length != 1:
            description = "\n".join(
                [
                    f"{Strings.number_emoji[idx]}{vote_item_list[idx + 1]}"
                    for idx in range(item_length - 1)
                ]
            )
            em = set_embed(message, title=vote_item_list[0], description=description)
            voted = await message.channel.send(embed=em)

            for i in range(item_length - 1):
                await voted.add_reaction(Strings.number_emoji[i])
            return
