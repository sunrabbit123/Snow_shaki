import discord
import datetime


def set_embed(ext: discord.Message, title: str = None, description: str = None):
    embed = discord.Embed(
        colour=0x7ACDF4, title=title, description=description, timestamp=ext.created_at
    )
    embed.set_footer(text=ext.author.name, icon_url=ext.author.avatar_url)
    return embed
