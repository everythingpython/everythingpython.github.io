from openai import AzureOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class AzureClient():
    def __init__(self):
        self.client = AzureOpenAI(azure_endpoint=os.getenv("azure_endpoint"),
                                      api_key=os.getenv("azureai_key"),
                                      api_version="2024-05-01-preview"
                                      )
        self.model = os.environ.get("azure_model")