import pymongo
from random import choice
import asyncio

class custom_command:
    def __init__(self, db):
        # db : mongodb database
        self.collect = db
    
    def command_insert(self, key, value, server, user) -> bool :
        self.collect.insert({"key-command" : key,
                            "value-command" : value,
                            "server" : server,
                            "user" : user})
        return True
    
    def command_select(self, message) -> str:
        key = ' '.join(message.content.split()[1:])
        result = list(self.collect.find({
            "key-command" : key
        },{
            "_id" : False,
            "key-command" : True,
            "value-command" : True,
            "server" : True,
            "user" : True
        }))
        return result

    def command_delete(self, key) -> bool :
        self.collect.remove({
            "key-command" : key
        })
        return True