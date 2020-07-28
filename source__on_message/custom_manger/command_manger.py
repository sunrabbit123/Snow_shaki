import asyncio
from models import made_command
import random
from db_manger import dbmanger
from models import made_command 
class command_manger():
    def __init__(self,message,prefixed = True):
        self.features = {'추가' : '_add' , '삭제' : '_delete' , '목록' : '_list'}    
        self.dbmanger = dbmanger()
        try :
            getattr(self,'command_custom' + self.features[message.content.split()[2]])(message,prefixed = True)
        except(IndexError,KeyError):
            message.channel.send("제대로 입력해주세요")

    async def command_custom_delete(self,message,prefixed = True):
        contents = message.content.split()[3]
        try:
            searching = self.dbmanger.search_data('made_command','keycommand',contents)
        except (IndexError):
            pass#추후에 커맨드 도움말 추가 
        else:
            if not searching:
                await message.add_reaction("\U00002753")
            server = str(message.guild.id)
            command_server = [command for command in searching if command.server == server]
            if command_server:
                for i in command_server:
                    self.dbmanger.delete_data(i)
                await message.content.channel.send("먀아,,,?\n그게 뭐야ㅏ,,")
    
    async def command_custom_list(self,message,prefixed = True):
        await message.channel.trigger_typing()

        server = str(message.guild.id)
        searched = self.dbmanger.search_data(made_command,"server_id",server)
        if not searched:
            await message.channel.send("야랄,,,,커맨드도,,없는데,,무슨,,")
            return
        diction_command = {}

        for command in searched:
            if command.keycommand in diction_command:
                diction_command[command.keycommand] += 1
            else:
                diction_command[command.keycommand] = 1
        
        title = "{}의 커맨드 목록".format(message.guild.name)
        description = "\n".join(["``%s``" % command for command in diction_command])

        
        await message.channel.send(title + "\n```" + description + "\n```")
        

    async def command_custom_add(self,message,prefixed = True):
        contents = message.content.split()
        server = message.guild
        server_id = message.guild.id
        author = message.author
        make_command = contents[2]
        make_output = contents[3:]

        made = made_command(server,server_id,author,make_command,make_output)

        self.dbmanger.insert_row(made)
        await message.channel.send("야랄,,, 근데 왜 나한테 이런걸ㄹ,,")