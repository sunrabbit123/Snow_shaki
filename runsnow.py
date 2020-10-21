from New_snowshaki import ShakiBot
from configparser import ConfigParser
import pymongo
config = ConfigParser()
config.read('config.ini')

token = config.get('default', 'token')
admin = config.get('default', 'admin')

connection = pymongo.MongoClient('mongodb://localhost:27017/')
db = connection.Shaki
collection = db.get_collection('Shaki_command')

print("와ㅏㅏ 실행된다ㅏㅏ")
ShakiBot(collection, admin = admin).run(token)


print("샤키가 사라졌다")

