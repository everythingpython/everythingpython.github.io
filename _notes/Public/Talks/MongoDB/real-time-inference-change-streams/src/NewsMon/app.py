from gevent import monkey
monkey.patch_all()  # Ensure all modules are patched before importing anything else

from flask import Flask, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_socketio import SocketIO
import time

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/newsDB"
mongo = PyMongo(app)
socketio = SocketIO(app, async_mode="gevent", cors_allowed_origins="*")

category_counts = {
    "Sports": 0,
    "Music": 0,
    "Movies": 0,
    "Global News": 0
}

@app.route('/')
def index():
    return render_template('index.html', counts=category_counts)

def watch_changes():
    """ Watches MongoDB for real-time changes and emits updates via WebSockets. """
    print("🔥 Starting MongoDB Change Stream Watcher...")  # Debugging
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["newsDB"]
        collection = db["articles"]

        print("✅ Watching MongoDB for changes...")  # Debugging

        with collection.watch() as stream:
            for change in stream:
                print("🔥 Detected change:", change)  # Debugging
                if change["operationType"] == "insert":
                    category = change["fullDocument"]["category"]
                    if category in category_counts:
                        category_counts[category] += 1
                        print(f"📢 Updating count for {category}: {category_counts[category]}")  # Debugging
                        socketio.emit("update_counts", category_counts)
    except Exception as e:
        print("❌ Error in watch_changes():", str(e))

if __name__ == '__main__':
    print("🚀 Starting Flask app...")
    time.sleep(1)  # Small delay to see print statements clearly

    print("🛠️ Spawning MongoDB watcher thread...")
    socketio.start_background_task(watch_changes)  # Run in background

    print("🟢 Running Flask with WebSockets...")
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)
