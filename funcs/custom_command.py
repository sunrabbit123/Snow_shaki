import discord


class CustomCommand:
    @staticmethod
    async def command_잊어(message: discord.Message, db):  # 샤키야 key커맨드
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
