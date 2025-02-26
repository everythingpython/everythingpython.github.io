from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
class OpenAIClient():
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("openai_key"))
        self.model = "gpt-4o"
