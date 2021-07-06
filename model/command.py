import pymongo


class CustomCommandModel:
    def __init__(self, db: pymongo.database.Database):
        # db : mongodb database
        self.collect: pymongo.collection.Collection = db.Shaki_command

    def command_insert(self, key, value, server, user) -> bool:
        try:
            self.collect.insert(
                {
                    "key-command": key,
                    "value-command": value,
                    "server": server,
                    "user": user,
                }
            )
            return True
        except Exception as err:
            print(err)
            return False

    def command_select(self, message) -> str:
        key = " ".join(message.content.split()[1:])
        result = list(
            self.collect.find(
                {"key-command": key},
                {
                    "_id": False,
                    "key-command": True,
                    "value-command": True,
                    "server": True,
                    "user": True,
                },
            )
        )
        return result

    def command_delete(self, key) -> bool:
        self.collect.remove({"key-command": key})
        return True
