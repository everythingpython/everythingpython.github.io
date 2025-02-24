from pymongo import MongoClient

import time
import random

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

import openai

import conf
# OpenAI API key
api_key = conf.api_key

def classify_article(article):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    prompt="Classify the following article into one of the categories: Sports, Music, Movies, Global News."

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content":prompt},
        {"role": "user", "content": str(article)}
    ]
    )

    print(completion.choices[0].message)

    category = completion.choices[0].message.content
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
    time.sleep(5)