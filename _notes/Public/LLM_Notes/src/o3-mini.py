from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

prompt = """
Write a bash script that takes a matrix represented as a string with 
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
"""

response = client.chat.completions.create(
    model="o3-mini",
    reasoning_effort="medium",
    messages=[
        {
            "role": "user", 
            "content": prompt
        }
    ]
)

print(response.choices[0].message.content)