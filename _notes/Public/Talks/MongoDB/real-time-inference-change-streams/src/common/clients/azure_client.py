from openai import AzureOpenAI
import os

# Create a file named config.py in the same directory as this file
# and add the following lines:
# azure_endpoint = "<deployment>"
# azureai_key="<azure key>"
# azure_model="<model name>"
from .config import azure_endpoint, azureai_key, azure_model

class AzureClient():
    def __init__(self):
        self.client = AzureOpenAI(azure_endpoint=azure_endpoint,
                                  api_key=azureai_key,
                                  api_version="2024-02-15-preview"
                                  )
        self.model = azure_model
