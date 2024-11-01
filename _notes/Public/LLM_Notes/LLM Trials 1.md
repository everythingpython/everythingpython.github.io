---
title: LLM Trials 1
feed: show
date: 2024-11-01
tags:
  - ollama
  - llms
---
_Date : 2024-11-01_

I've been trying a lot of stuff with LLMs over the last 18 months or so. These trial posts have been a long time coming. 

I set up Ollama a few months ago and the model I'm using locally currently - `llama3.1:8b` .

The request body for Ollama's suite of APIs follows a pattern like - 

```json
{  
    "model": "llama3.1:8b",  
    "prompt": "<user_prompt>",  
    "system": "<system_prompt>",  
    "stream": False
}
```


---

But this article is going to focus on using Python's APIs . I'm using Instructor here . Too sleepy to go into the depth of stuff - 

In this example, I'm trying to fetch the names of cities from a string. 
For this, I will be using a Pydantic Class that returns a List of strings. 

The system prompt I've set for this is - "You are a city identifier. Return the names of cities as a list from the sentence provided"

```python

from typing import List  
import instructor  
from openai import OpenAI  
from pydantic import BaseModel  
  
  
full_string = "The weather in Chennai is a lot hotter than in Bangalore."  
  
  
class Cities(BaseModel):  
    cities: List[str]  
  
  
# enables `response_model` in create call  
client = instructor.from_openai(  
    OpenAI(  
        base_url="http://localhost:11434/v1",  
    ),  
    mode=instructor.Mode.JSON,  
)  
  
resp = client.chat.completions.create(  
    model="llama3.1:8b",  
    messages=[  
        {  
            "role": "system",  
            "content": "You are a city identifier. Return the names of cities from the sentence provided.",  
        },  
        {  
            "role": "user",  
            "content": f"{full_string}",  
        },  
    ],  
    response_model=Cities,  
)  
print(resp.model_dump_json(indent=2))

```


**This is the response -** 

```json
{
  "cities": [
    "Chennai",
    "Bangalore"
  ]
}
```

Solid stuff. The reason this structure is achievable is because of Instructor though. When I used the API call without instructor, it was always a string returned. 