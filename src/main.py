'''Full orchestration of the project
takes creates a conversation loop
store the queries into the cache
each time ask as if cache has seen before, if not llm
if yes throw back previous answer
'''
import uuid
from src.cache import Cache
from src.embeddings import Embedding
from src.session_manager import SessionManager
from dotenv import load_dotenv
import os
from google import genai
import time
import numpy as np



load_dotenv()
key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=key)

session_id = np.random.randint(1, 31)
session_manager = SessionManager()
embedding = Embedding(key)
cache = Cache()
avg_time = []
total_calls, cache_hits = 0, 0
start = time.time()



while (True):
    user_input = input("Please type your work: ")
    if user_input.lower() in ["quit", "exit"]:
        break
    similarity_score = 0.78 # change this to a better way to calculate similarity score
    context = session_manager.get_context(session_id)
    # history = "\n".join([
    #     f"User: {t['user']}"
    #     for t in context
    # ])
    # full_prompt = f"{history}\nUser: {user_input}"

    # full_prompt = build_context_embedding(user_input, history, embedding)
    start = time.time()
    response = cache.search_cache(similarity_score=similarity_score, query=user_input, history=context)
    total_calls += 1
    if response == (None, None, None):
        print("AI ✅")
        # throw it to the llm
        ai_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_input
        )
        print(ai_response.text)
        # store the response in cache for next time
        cache.add_to_cache(query=user_input, response=ai_response.text, session_id=session_id)
        session_manager.add_turn(session_id=session_id, user_msg=user_input, ai_msg=ai_response.text)
        end = time.time()

    else: 
        # give back to the user and dont store the same answer
        # print(response['response'])
        cache_hits += 1
        session_manager.add_turn(session_id=session_id, user_msg=user_input, ai_msg=response)
        print("CACHE ✅")
        print(response["response"])
        end = time.time()


    latency = end - start
    avg_time.append(latency)
print(np.mean(avg_time))
hit_rate = cache_hits / total_calls
    
    