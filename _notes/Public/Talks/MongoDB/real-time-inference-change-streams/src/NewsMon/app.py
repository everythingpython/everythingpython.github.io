from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
import threading
import json
import requests

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/newsDB"
mongo = PyMongo(app)

# Dictionary to store category counts
category_counts = {
    "Sports": 0,
    "Music": 0,
    "Movies": 0,
    "Global News": 0
}

@app.route('/')
def index():
    return render_template('index.html', counts=category_counts)

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    category = data.get('category')
    if category in category_counts:
        category_counts[category] += 1
    return '', 204

def watch_changes():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['newsDB']
    collection = db['articles']
    with collection.watch() as stream:
        for change in stream:
            if change['operationType'] == 'insert':
                category = change['fullDocument']['category']
                requests.post('http://localhost:5000/update', json={'category': category})

if __name__ == '__main__':
    watcher_thread = threading.Thread(target=watch_changes, daemon=True)
    watcher_thread.start()
    app.run(debug=True)
