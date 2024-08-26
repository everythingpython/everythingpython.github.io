import urllib, urllib.request, json
import requests
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

from keys import *
from openai import OpenAI

anthropic = Anthropic(api_key=anthropic)
openai_k = openai_key


url = "https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty"
data = urllib.request.urlopen(url)
data = json.loads(data.read().decode("utf-8"))


d_ict = {"name": [], "url": []}
for i in list(data)[1:3]:
    url = f"https://hacker-news.firebaseio.com/v0/item/{i}.json?print=pretty"
    data = urllib.request.urlopen(url)
    json_data = json.loads(data.read().decode("utf-8"))
    d_ict["name"].append(json_data.get("title", ""))
    d_ict["url"].append(json_data.get("url", ""))

try:
    content_full = []
    for name, url in zip(d_ict["name"], d_ict["url"]):
        if url:
            content_d = {}
            print(f"Processing {url}")
            response = requests.get(url)
            content = response.text[1:1000]
            content_d["name"] = name
            content_d["url"] = url
            content_d["content"] = content
            content_full.append(content_d)

    from pydantic import BaseModel

    class AIResponse(BaseModel):
        name: str
        url: str
        topic: str

    class AIResponseList(BaseModel):
        responses: list[AIResponse]

    # Define the response model
    response_model = AIResponseList

    messages = [
        {
            "role": "user",
            "content": f"Please go through the content and for each title return the topic of the content. If it's about Python, return Python. If it's about GenAI, return GenAI. Else return irrelevant:\n\n{content_full}",
        }
    ]
    client = OpenAI(api_key=openai_k)

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06", messages=messages, response_format=response_model
    )

    # The response will now be forced to be either "Python" or "GenAI"
    topic = completion.choices[0].message.parsed

    print(f"The content is:\n {topic}")
except Exception as e:
    print(f"Error processing {url}: {str(e)}")
