from bot import ShakiBot
import os
import pymongo

token = os.environ["TOKEN"]
admin = os.environ["admin"]
db_path = os.environ["db"]

if __name__ == "__main__":
    client = pymongo.MongoClient(db_path)
    db = client.get_database("Shaki")
    print("Complete connect database")
    ShakiBot(db, admin=admin).run(token)

print("It has been terminated.")
