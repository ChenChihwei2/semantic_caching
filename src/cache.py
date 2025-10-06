# store the cache and search for the cache functions
import chromadb
from chromadb.config import Settings
from chromadb import Client
from src.embeddings import Embedding
from dotenv import load_dotenv
import uuid
import os

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

class Cache:
    def __init__(self):
        # self.client = chromadb.PersistentClient() when you want to store the information more long term
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(name = "semantic_cache", metadata={"hnsw:space": "cosine"})
        self.emb = Embedding(api_key=key)

    def add_to_cache(self, query, response, session_id):
        embedding = self.emb.get_embedding(content=query)
        unique_id = str(uuid.uuid4())
        self.collection.add(
            embeddings=[embedding],
            metadatas=[{"query": query, "session_id": session_id}],
            documents=[response],
            ids=[unique_id]
        )
        return
    def build_context_embedding(self, query, history, model):
        context = " ".join(turn['user'] for turn in history[-2:])  # last 2 turns
        text = f"Context: {context}\nQuery: {query}"
        return model.get_embedding(text)
    
    def search_cache(self, similarity_score, query, history):

        # embedding = self.emb.get_embedding(content=query)
        embedding = self.build_context_embedding(query, history, self.emb)
        # embedding = query
        if self.collection.count() == 0:
            return None, None, None
        results = self.collection.query(
            query_embeddings=[embedding], 
            n_results=1
        )
        best_score = 1 - results["distances"][0][0]
        if best_score >= similarity_score:
            return {
                "response": results["documents"][0][0],
                "score": best_score,
                "metadata": results["metadatas"][0][0]
            }
    
        return None, None, None