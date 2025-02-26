from pymongo import MongoClient
import os 
import time
import random
import sys
from opik import track
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.llm_utils import invoke_llm


os.environ["OPIK_URL_OVERRIDE"] = "http://localhost:5173/api"
# Sample templates for each category
templates = {
    "Sports": "Breaking: Local team wins championship game.",
    "Music": "New album release tops the charts this week.",
    "Movies": "Upcoming blockbuster set to hit theaters soon.",
    "Global News": "International summit addresses climate change."
}

def generate_article():
    category = random.choice(list(templates.keys()))
    article = {
        "title": templates[category],
        "content": f"Details about {category.lower()} event.",
        "category": category
    }
    return article

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['newsDB']
collection = db['articles']


@track
def classify_article(article):
    sys_prompt="Classify the following article into one of the categories: Sports, Music, Movies, Global News."
    user_prompt = str(article)
    category = invoke_llm(sys_prompt, user_prompt)
    return category

# Inside the article insertion function
def insert_article(article):
    category = classify_article(article)
    article['category'] = category
    collection.insert_one(article)
    print(f"Inserted article into MongoDB: {article['title']} with category: {category}")

# Inside the article generation loop
while True:
    article = generate_article()
    insert_article(article)
    time.sleep(10)


    