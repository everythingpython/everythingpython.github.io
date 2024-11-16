import json

import requests


def list_models():
    url = "http://localhost:11434/api/tags"  # Listing the models
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    formatted_response = json.dumps(response.json(), indent=4)
    return formatted_response


def chat():
    url = "http://localhost:11434/api/chat"

    payload = json.dumps({
        "model": "llama3.2:latest",
        "messages": [
            {
                "role": "system",
                "content": f"{sys_message}"
            },
            {
                "role": "user",
                "content": f"{user_message}"
            }
        ],
        "stream": False
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["message"]["content"]


def main(mode):
    response = None
    if mode == "list":
        response = list_models()
    elif mode == "chat":
        response = chat()
    return response


sys_message = "You are an algorithms expert."
user_message = ("For a list of numbers where I have to check for duplicates, for what value of n does nlogn become "
                "faster than n?")
m_response = main("chat")
print(m_response)
