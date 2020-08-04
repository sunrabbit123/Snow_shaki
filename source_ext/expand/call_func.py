from const import Strings
from custom_manger import command_manger
import discord

def command_find(command,prefixed = True):
    diction = getattr(Strings,'command_prefixes' if prefixed else 'command_not_prefixes')
    for commands, string in diction.items():
        if command in string:
            return commands

class call_func:
    def __init__(self):
        self.Prefix_list = Strings.Prefix

    def func_find(self, message: discord.message, prefixed = True):
        command = message.content.split()[prefixed]
        print(f"{command}")
        command = command_find(command, prefixed=prefixed)
        if command is None:
            return
        return f"command_{command}"

    def func_get(self, message : discord.Message):
        contents = message.content.split(" ")
        print(contents)
        try:
            if contents[0] in self.Prefix_list:
                print("if")
                
                return self.func_find(message)
            else:
                print("else")
                contents = contents[0]
                return self.func_find(message, prefixed = False)
        except:
            return

        
        
        