import discord

from model import CustomCommandModel as CCM


class CustomCommand:
    @staticmethod
    async def command_잊어(message: discord.Message, db):  # 샤키야 key커맨드
        key = message.content.split()[2]
        result = CCM(db).command_delete(key)

        if result:
            await message.channel.send("그게,,, 뭐죠,,,?")

    @staticmethod
    async def command_배워(message: discord.Message, db):  # 샤키야 배워 key커맨드 value커맨드
        word = " ".join(message.content.split()[2:]).split(":")
        key_command = word[0]
        value_command = ":".join(word[1:])
        CCM(db).command_insert(
            key_command, value_command, message.channel.name, message.author.name
        )
        # key, value, server, user

        await message.channel.send("야랄 왜 나한테...")
