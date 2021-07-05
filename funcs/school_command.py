import re

import discord

from utils import set_embed, get_date, SearchWord
from const import Strings


class SchoolCommand:
    @staticmethod
    async def command_시간표(message: discord.message):
        return None

    @staticmethod
    async def command_급식(message: discord.message, db):
        word = message.content.split()[1:]
        dates = get_date(message)

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

            em = set_embed(
                message,
                title=f"{dates.strftime()}",
                description=meal_list[0]["SCHUL_NM"],
            )
            if meal_type == "급식":
                meal = list()

                def meal_filtering(meal: str, CAL_INFO: str):
                    meal = re.sub(pattern="[^가-힣|</br>]", repl="", string=str(meal))
                    meal = "\n".join(meal.split("<br/>"))
                    meal += f"\n{CAL_INFO}"
                    return meal

                for i in range(0, 3):
                    em.add_field(
                        name=meal_list[i]["MMEAL_SC_NM"],
                        value=meal_filtering(
                            meal_list[i]["DDISH_NM"], meal_list[i]["CAL_INFO"]
                        ),
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
