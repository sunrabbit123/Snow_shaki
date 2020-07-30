from .base_func import base_func
from const import Strings
from custom_manger import command_manger
import discord

def command_find(message,prefixed = True):
    diction = getattr(Strings,'command_prefixes' if prefixed else 'commands')
    for command, string in diction.items():
        if message in string:
            return command

class call_func:
    def __init__(self):
        self.Prefix_list = Strings.Prefix
        self.Expand_func = base_func()

    def func_find(self, message: discord.message, prefixed = True):
        command = message.content.split()[prefixed]
        command = command_find(f"command_{command}",prefixed=prefixed)
        func = getattr(self.Expand_func, f"command_{command}")
        return func

    def func_get(self, message : discord.Message):
        contents = message.content.split()
        if self.Prefix_list in contents:
            contents = contents[1]
            return self.func_find(message)
        else:
            contents = contents[0]
            return self.func_find(message, prefixed = False)

        
        
        