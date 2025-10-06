from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Give me the lyrics to Happy by Marshmello"
)
print(response.text)
