from New_snowshaki import ShakiBot
from configparser import ConfigParser
import pymongo
config = ConfigParser()
config.read('config.ini')

token = config.get('default', 'token')
admin = config.get('default', 'admin')
db_path = config.get('default', 'db')
print(db_path)
connection = pymongo.MongoClient(db_path, port=27017)
print(connection)
db = connection.test

print(db)
print("complete connect db")
collection = db.get_collection('Shaki_command')

print("와ㅏㅏ 실행된다ㅏㅏ")
ShakiBot(collection, admin = admin).run(token)


print("샤키가 사라졌다")

