from New_snowshaki import ShakiBot
import os
import pymongo

token = os.environ["TOKEN"]
admin = os.environ['admin']
db_path = os.environ['db']

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

