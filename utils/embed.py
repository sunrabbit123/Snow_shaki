import discord


def set_embed(ext: discord.Message, title: str = None, description: str = None):
    embed = discord.Embed(
        colour=0x7ACDF4, title=title, description=description, timestamp=ext.created_at
    )
    embed.set_footer(text=ext.author.name, icon_url=ext.author.avatar_url)
    return embed


def not_found_school(ext: discord.Message):
    return set_embed(
        ext, description="야발,, 학교도 등록이 안되어있는데 뭘ㄹ,,\n**샤키야 학교검색 학교이름**이라고 해보던가,,"
    )
