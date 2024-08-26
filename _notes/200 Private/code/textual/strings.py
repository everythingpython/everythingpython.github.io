def get_sys_prompt(content_full):
    prompt = f"Please go through the content and for each title \
    return the topic of the content. If it's about Python, return Python. \
    If it's about GenAI, return GenAI. Else return irrelevant:\n\n{content_full}"

    return prompt


hacker_news_latest_url = "https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty"
def hacker_news_get_article_url(i):
    return f"https://hacker-news.firebaseio.com/v0/item/{i}.json?print=pretty"
