# Test whether any type of input from user can be translated into embedding array
from google import genai
from dotenv import load_dotenv
import os
import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
from src.embeddings import Embedding

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=key)

question = "What is the meaning of life?"

emb = Embedding(api_key=key)
result = emb.get_embedding(content=question)

# Add logging in the future
assert(type(result) == list)
print("~Test Passed~")
