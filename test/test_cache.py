# test_cache.py
from src.cache import Cache
from dotenv import load_dotenv
import os
import time

# Load environment variables (for GEMINI_API_KEY)
load_dotenv()

def test_cache_basic():
    print("=== Cache Test: Basic Add + Search ===")
    cache = Cache() 

    session_id = "test_session_1"
    threshold = 0.85

    q1 = "What is the capital of France?"
    r1 = "The capital of France is Paris."

    q2 = "Tell me the capital of France."  # semantically similar to q1
    q3 = "What is the population of Japan?"  # different
    # # Step 0: Test if you can search without adding in features
    print("\nSearching cache with a paraphrased query...")
    hit = cache.search_cache(query = q1, similarity_score=threshold)
    if hit == (None, None, None):
        print(f"Correctly returns nothing ✅")
    else:
        print("Error ❌")

    # Step 1: Add first query + response to cache
    print("Adding first Q&A pair to cache...")
    cache.add_to_cache(q1, r1, session_id=session_id)

    # Step 2: Test near-duplicate query
    print("\nSearching cache with a paraphrased query...")
    hit = cache.search_cache(query = q2, similarity_score=threshold)
    if hit:
        print(f"CACHE HIT ✅\nSimilarity: {hit['score']:.4f}\nResponse: {hit['response']}")
    else:
        print("CACHE MISS ❌")

    # Step 3: Test totally different query
    print("\nSearching cache with an unrelated query...")
    miss = cache.search_cache(query = q3, similarity_score=threshold)
    if miss:
        print(f"Unexpected hit: {miss}")
    else:
        print("Correctly returned MISS ✅")

    # Step 4: Optional performance test
    print("\nAdding multiple entries for latency test...")
    for i in range(5):
        cache.add_to_cache(f"What is item {i}?", f"Answer {i}", session_id=session_id)

    start = time.time()
    cache.search_cache(query = "Tell me about item 4", similarity_score=0.8)
    print(f"Search latency: {time.time() - start:.4f} seconds")

test_cache_basic()
