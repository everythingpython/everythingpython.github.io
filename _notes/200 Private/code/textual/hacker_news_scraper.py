import json
import os
import urllib.request

import requests
from anthropic import Anthropic
from openai import OpenAI
from pydantic import BaseModel

from keys import *

anthropic = Anthropic(api_key=anthropic)
openai_k = openai_key

url = "https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty"
data = urllib.request.urlopen(url)
data = json.loads(data.read().decode("utf-8"))

existing_urls = set()
if os.path.exists("topic_analysis.json"):
    with open("topic_analysis.json", "r") as json_file:
        existing_data = json.load(json_file)
        if "responses" in existing_data:
            existing_urls = {item["url"] for item in existing_data["responses"]}
print(f"Before = {len(data)}")

d_ict = {"name": [], "url": []}
for i in list(data)[1:10]:
    url = f"https://hacker-news.firebaseio.com/v0/item/{i}.json?print=pretty"
    data = urllib.request.urlopen(url)
    json_data = json.loads(data.read().decode("utf-8"))
    d_ict["name"].append(json_data.get("title", ""))
    d_ict["url"].append(json_data.get("url", ""))

try:
    content_full = []
    try:
        for name, url in zip(d_ict["name"], d_ict["url"]):
            if url not in existing_urls:
                content_d = {}
                print(f"Processing {url}")
                response = requests.get(url)
                content = response.text[1:1000]
                content_d["name"] = name
                content_d["url"] = url
                content_d["content"] = content
                content_full.append(content_d)
    except Exception as e:
        print("Skipping {}".format(url))
        pass
    print(f"Total URLs to process - {len(content_full)} ")

    class AIResponse(BaseModel):
        name: str
        url: str
        topic: str

    class AIResponseList(BaseModel):
        responses: list[AIResponse]

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

    if topic:
        # Convert the topic object to a dictionary
        topic_dict = topic.model_dump()

        # Convert the dictionary to JSON
        topic_json = json.dumps(topic_dict, indent=2)
        json_filename = f"topic_analysis.json"

        # Read existing JSON data from the file
        existing_data = {}
        if os.path.exists(json_filename):
            with open(json_filename, "r") as json_file:
                existing_data = json.load(json_file)

        # Filter out irrelevant topics
        new_responses = [
            response
            for response in topic_dict["responses"]
            if response["topic"].lower() != "irrelevant"
        ]
        topic_dict["responses"] = new_responses
        # Merge existing data with new data
        if "responses" in existing_data:
            existing_data["responses"].extend(topic_dict["responses"])
        else:
            existing_data = topic_dict

        # Convert the merged data back to JSON
        topic_json = json.dumps(existing_data, indent=2)
        # Write the merged data to the JSON file
        with open(json_filename, "w") as json_file:
            json_file.write(topic_json)
        print(f"JSON output written to {json_filename}")

    print(f"The content is:\n {topic}")
except Exception as e:
    print(f"Error processing {url}: {str(e)}")
