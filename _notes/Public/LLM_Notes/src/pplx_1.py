import requests
from dotenv import load_dotenv
import os

load_dotenv()

response = requests.post(
    'https://api.perplexity.ai/chat/completions',
    headers={
        'Authorization': f"Bearer {os.getenv('PPLIXTY_KEY')}",
        'Content-Type': 'application/json'
    },
    json={
        'model': 'sonar-pro',
        'messages': [
            {
                'role': 'user',
                'content': "Look up https://everythingpython.substack.com/p/revisiting-postgres-1 and score it as a blog post."
            }
        ]
    }
)

print(response.json())