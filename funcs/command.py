import discord

import random
import re
import os

from utils import set_embed, get_date
from const import Docs, Strings
from web_find import SearchWord


class basic_command:
    @staticmethod
    async def command_help(message):
        em = set_embed(message, title="샤키의 도움말 목록")
        for i in range(len(Docs.help_title)):
            em.add_field(
                name=Docs.help_title[i], value=Docs.help_description[i], inline=False
            )
        em.set_footer(text=Docs.NH)
        await message.channel.send(embed=em)

    @staticmethod
    async def command_clean_messages(message):
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
    async def command_emoji(message):
        await message.channel.send(random.choice(Strings.emoji))

    @staticmethod
    async def command_choice(message):
        chlist = message.content.split()[2:]
        await message.channel.send(f"내가 뽑은건...!\n{random.choice(chlist)}입니당!")

    @staticmethod
    async def command_굴러(message):
        await message.channel.send(Strings.roll)

    @staticmethod
    async def command_구글검색(message):
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
    async def command_사전검색(message):
        findn = " ".join(message.content.split()[2:])
        findit = await SearchWord().get_dic(findn)

        if findit is None:
            await message.channel.send("사전검색이 실패했습니다.")

        else:
            em = set_embed(message, title=f"{findn}의 네이버 사전검색 결과", description=findit)
            await message.channel.send(embed=em)

    @staticmethod
    async def command_급식(message):
        word = message.content.split()[1:]
        dates = get_date(message)
        em = set_embed(message, title=f"{dates.strftime()}")

        # meal_list[0] == 조식
        # meal_list[1] == 중식
        # meal_list[2] == 석식

        meal_type = (
            "조식"
            if "조식" in word or "아침" in word
            else "중식"
            if "중식" in word or "점심" in word
            else "석식"
            if "석식" in word or "저녁" in word or "저녘" in word
            else "급식"
        )
        meal = None

        try:
            meal_list = (await SearchWord.get_meal(dates.url_date()))[
                "mealServiceDietInfo"
            ][1]["row"]
            if meal_type == "급식":
                meal = list()

                def meal_filtering(meal: str):
                    meal = re.sub(pattern="[^가-힣|</br>]", repl="", string=str(meal))
                    meal = "\n".join(meal.split("<br/>"))
                    return meal

                for i in range(0, 3):
                    em.add_field(
                        name=meal_list[i]["MMEAL_SC_NM"],
                        value=meal_filtering(meal_list[i]["DDISH_NM"]),
                        inline=True,
                    )
            else:
                meal = meal_list[Strings.meal_dict[meal_type]]["DDISH_NM"]
                meal = re.sub(pattern="[^가-힣|</br>]", repl="", string=str(meal))
                meal = "\n".join(meal.split("<br/>"))
                em.add_field(name=meal_type, value=meal, inline=True)
        except KeyError:
            em.add_field(name="오류", value="급식이 없습니다.")
        except IndexError:
            pass
        await message.channel.send(embed=em)

        # try :
        #     if meal_type == "급식":
        #         meal_type_list = ["조식", "중식", "석식"]
        #         for i in range(0,3):
        #             meal = meal_list
        #             em.add_field(name = meal_type_list[i], value = meal[i])

    @staticmethod
    async def command_링크(message):
        await message.channel.send(
            discord.utils.oauth_url(
                client_id=os.environ["client"],
                permissions=discord.Permissions(permissions=1610837057),
            )
        )
        await message.channel.send("여기 있어요,,,")


class custom_command:
    @staticmethod
    async def command_잊어(message, db):  # 샤키야 key커맨드
        key = message.content.split()[2]
        result = db.command_delete(key)

        if result:
            await message.channel.send("그게,,, 뭐죠,,,?")

    @staticmethod
    async def command_배워(message: discord.Message, db):  # 샤키야 배워 key커맨드 value커맨드
        word = " ".join(message.content.split()[2:]).split(":")
        db.command_insert(word[0], word[1], message.channel.name, message.author.name)
        # key, value, server, user

        await message.channel.send("야랄 왜 나한테...")
