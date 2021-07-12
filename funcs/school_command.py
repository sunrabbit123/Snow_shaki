import discord
from discord.ext.commands import Bot

import asyncio
import re

from utils import get_date, set_embed, get_date, NeisAPI, not_found_school, StringManger
from const import Strings
from model import SchoolCommandModel as SC


class SchoolCommand:
    @staticmethod
    async def command_시간표(message: discord.message, db):
        date = get_date(message)
        school = None
        data = None
        try:# TODO 길드가 없을경우 (갠디일 경우) 처리 필요
            school: dict = await (SC(db)).get_school(message.guild.id, message.channel.id)
            
            data: dict = {
                "ATPT_OFCDC_SC_CODE": school["ATPT_OFCDC_SC_CODE"],
                "SCHOOL_INFO": school["SCHOOL_CODE"],
                "ALL_TI_YMD": date.url_date(),
            }
            data["SCHUL_KND_SC_NM"] = school["SCHUL_KND_SC_NM"]
        except KeyError:
            em = not_found_school(message)
            await message.channel.send(embed=em)
            return
            
        content = message.content
        data["GRADE"] = StringManger.get_grade(content)
        data["CLASS_NM"] = StringManger.get_class(content)
        embed = None
        try:
            search_result = (await NeisAPI.get_schedule(**data))[
                Strings.school_type[school["SCHUL_KND_SC_NM"]]
            ][1]["row"]
            print(search_result)
            embed = set_embed(
                message,
                title=f"{date.strftime()}",
                description="%s\n%s"
                % (
                    search_result[0]["SCHUL_NM"],
                    data["GRADE"] + "학년 " + data["CLASS_NM"] + "반",
                ),
            )
            regacy = None
            for i in search_result:
                if i["PERIO"] == regacy:
                    continue
                embed.add_field(
                    name="%s교시" % i["PERIO"], value=i["ITRT_CNTNT"], inline=False
                )
                regacy = i["PERIO"]
        except KeyError:
            embed = set_embed(
                message, title="검색결과가 없습니다.", description="그니까 똑바로 검색하라고 ㅡㅡ,,,,"
            )
        finally:
            await message.channel.send(embed=embed)

    @staticmethod
    async def command_regist(message: discord.message, db, client: Bot):
        school_name = message.content.split()[2]

        try:
            search_result = (await NeisAPI.search_school(school_name))["schoolInfo"][1][
                "row"
            ]
        except KeyError:
            await message.channel.send(
                embed=set_embed(
                    message, title="검색결과가 없습니다.", description="그니까 똑바로 검색하라고 ㅡㅡ,,,,"
                )
            )
            return

        em = set_embed(message, title="검색 결과")
        for idx, result in enumerate(search_result):
            em.add_field(
                name=f"{idx + 1}. %s" % result["SCHUL_NM"],
                value="%s" % result["ORG_RDNMA"],
                inline=False,
            )

        msg = await message.channel.send(embed=em)

        number_emoji = Strings.number_emoji[: len(search_result)]
        for i in number_emoji:
            await msg.add_reaction(i)
        # 이모지달기

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in number_emoji

        try:
            reaction, user = await client.wait_for(
                "reaction_add", timeout=30.0, check=check
            )
        except asyncio.TimeoutError:
            await msg.edit(
                embed=set_embed(
                    message,
                    title="시간 초과",
                    description="야랄,, 불러놓고 대답을 안하네\n30초만 기다릴거니까 그 안에 누르라고;;\n아무튼 등록취소야,,,",
                )
            )
            await msg.clear_reactions()
        else:
            index: int = Strings.number_emoji_dict[
                str(reaction.emoji)
            ]  # 이모지에 해당하는 인덱스값 구하기
            school: dict = search_result[index]  # 이모지에 해당하는 인덱스값으로 학교 조회
            school_con = SC(db)
            try:
                await school_con.delete_school(message.guild.id, message.channel.id)
                await school_con.register(
                    message.guild.id,
                    message.channel.id,
                    school["ATPT_OFCDC_SC_CODE"],
                    school["SD_SCHUL_CODE"],
                    school["SCHUL_KND_SC_NM"],
                )
            except Exception as err:
                print(err)
            await msg.edit(
                embed=set_embed(message, title="", description="성공적으로 처리되었습니다 :D")
            )
            await msg.clear_reactions()

    @staticmethod
    async def command_급식(message: discord.message, db):
        word = message.content.split()[1:]
        dates = get_date(message)
        try:
            school: dict = await (SC(db)).get_school(message.guild.id, message.channel.id)
        except KeyError:
            em = not_found_school(message)
            await message.channel.send(embed=em)
            return
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
            meal_list = (
                await NeisAPI.get_meal(
                    dates.url_date(),
                    school["ATPT_OFCDC_SC_CODE"],
                    school["SCHOOL_CODE"],
                )
            )["mealServiceDietInfo"][1]["row"]

            em = set_embed(
                message,
                title=f"{dates.strftime()}",
                description=meal_list[0]["SCHUL_NM"],
            )

            def meal_filtering(meal: str, CAL_INFO: str):
                meal = StringManger.filter_without_dot_and_korean(meal)
                meal = StringManger.dots_to_new_line(meal)
                meal += f"{CAL_INFO}"
                return meal

            if meal_type == "급식":
                meal = list()

                for i in range(0, 3):
                    em.add_field(
                        name=meal_list[i]["MMEAL_SC_NM"],
                        value=meal_filtering(
                            meal_list[i]["DDISH_NM"], meal_list[i]["CAL_INFO"]
                        ),
                        inline=True,
                    )
            else:
                meal = meal_list[Strings.meal_dict[meal_type]]
                meal = meal_filtering(meal["DDISH_NM"], meal["CAL_INFO"])
                em.add_field(name=meal_type, value=meal, inline=True)

        except KeyError:
            em.add_field(name="오류", value="급식이 없습니다.")
        except TypeError:
            # school이 None일때
            em = not_found_school(message)
        except IndexError:
            pass
        await message.channel.send(embed=em)

        # try :
        #     if meal_type == "급식":
        #         meal_type_list = ["조식", "중식", "석식"]
        #         for i in range(0,3):
        #             meal = meal_list
        #             em.add_field(name = meal_type_list[i], value = meal[i])
