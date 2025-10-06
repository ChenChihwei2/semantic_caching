# You want to write function to obtain embeddings from text input 
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

class Embedding:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def get_embedding(self, content):
        ''' 
        Add sliding window to only keep relevant information
        '''

        response = self.client.models.embed_content(
            model="text-embedding-004",
            contents=content
        )
        return response.embeddings[0].values
