from .base_func import base_func
from const import Strings
from custom_manger import command_manger
import discord

def command_find(message,prefixed = True):
    diction = getattr(Strings,'command_prefixes' if prefixed else 'command_not_prefixes')
    for command, string in diction.items():
        if message in string:
            return command

class call_func:
    def __init__(self):
        self.Prefix_list = Strings.Prefix
        self.Expand_func = base_func()

    def func_find(self, message: discord.message, prefixed = True):
        command = message.content.split()[prefixed]
        print(f"{command}\n{prefixed}")
        command = command_find(message, prefixed=prefixed)
        print(self.Expand_func)
        func = getattr(self.Expand_func, f"command_{command}")
        return func

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

        
        
        