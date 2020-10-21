import datetime

def print_time(func):
    async def wrapper(self, message):
        print(datetime.datetime.now(), end = ' ')
        return await func(self, message)
    return wrapper