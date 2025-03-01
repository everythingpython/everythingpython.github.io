from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["newsDB"]
collection = db["articles"]

print("Listening for changes...")
with collection.watch() as stream:
    for change in stream:
        print("Detected change:", change)
