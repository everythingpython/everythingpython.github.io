from gevent import monkey
monkey.patch_all()  # Ensures WebSockets and MongoDB work properly

from flask import Flask, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/newsDB"
mongo = PyMongo(app)
socketio = SocketIO(app, async_mode="gevent", cors_allowed_origins="*")

# ✅ Fetch Initial Counts from MongoDB
def get_initial_counts():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["newsDB"]
    collection = db["articles"]

    initial_counts = {
        "Sports": collection.count_documents({"category": "Sports"}),
        "Music": collection.count_documents({"category": "Music"}),
        "Movies": collection.count_documents({"category": "Movies"}),
        "Global News": collection.count_documents({"category": "Global News"}),
    }
    print("📊 Initial category counts:", initial_counts)  # Debugging print
    return initial_counts

# Initialize the category counts from the database
category_counts = get_initial_counts()

@app.route('/')
def index():
    return render_template('index.html', counts=category_counts)

# ✅ MongoDB Change Stream Watcher
def watch_changes():
    """ Watches MongoDB for real-time changes and emits updates via WebSockets. """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["newsDB"]
    collection = db["articles"]

    print("✅ Watching MongoDB for changes...")

    with collection.watch() as stream:
        for change in stream:
            if change["operationType"] == "insert":
                category = change["fullDocument"]["category"]
                if category in category_counts:
                    category_counts[category] += 1
                    print(f"📢 Updating count for {category}: {category_counts[category]}")
                    socketio.emit("update_counts", category_counts)

if __name__ == '__main__':
    print("🚀 Starting Flask app...")
    socketio.start_background_task(watch_changes)  # Run in the background
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)
