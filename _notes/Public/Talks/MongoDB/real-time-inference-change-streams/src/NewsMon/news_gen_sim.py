from pymongo import MongoClient
import os
import time
import random
import sys
from opik import track

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.llm_utils import invoke_llm

import pandas as pd

os.environ["OPIK_URL_OVERRIDE"] = "http://localhost:5173/api"
# Sample templates for each category

news_articles = pd.read_csv("./data/Random_News_Titles_from_India.csv")
news_articles_dict = news_articles.to_dict()
items_ = {}
for i in range(len(news_articles_dict["Category"])):
    cat = news_articles_dict["Category"][i]
    if not items_.get(cat):
        items_[cat] = [news_articles_dict["Title"][i]]
    else:
        items_[cat].append(news_articles_dict["Title"][i])



def generate_article():
    category = random.choice(list(items_.keys()))
    article = {
        "title": random.choice(items_[category]),
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
    sys_prompt = "Classify the following article into one of the categories: Tech, Politics, Sports, Entertainment, Misc."
    user_prompt = str(article)
    category = invoke_llm(sys_prompt, user_prompt, provider="azure")
    return category


# Inside the article insertion function
def insert_article(article):
    category = classify_article(article)
    article['category'] = category

    collection.insert_one(article)
    print(f"Inserted article into MongoDB: {article['title']} with category: {category}")


# Inside the article generation loop
while True:
    article_ = generate_article()
    insert_article(article_)
    time.sleep(10)
