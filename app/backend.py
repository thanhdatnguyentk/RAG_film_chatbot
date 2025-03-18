from pymongo import MongoClient
from pymongo.server_api import ServerApi
from sentence_transformers import SentenceTransformer
import os

class MongoDb:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("Missing MONGO_URI in environment variables")
        
        self.client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        self.db = self.client["sample_mflix"]
        self.collection = self.db["embedded_movies"]
        self.embedding_model = SentenceTransformer("thenlper/gte-large")

    def get_embeddings(self, text: str) -> list[float]:
        if not text.strip():
            print("No input text provided")
            return []
        return self.embedding_model.encode(text).tolist()

    def vector_search(self, user_query: str):
        """
        Perform a vector search on the collection using the user query
        """
        query_embedding = self.get_embeddings(user_query)
        if not query_embedding:
            return []

        pipeline = [
            {"$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_embedding,
                "path": "plot_embedding",
                "numCandidates": 150,
                "limit": 5
            }},
            {"$unset": "embedding"},
            {"$project": {
                "_id": 0,
                "title": 1,
                "fullplot": 1,
                "genres": 1,
                "year": 1,
                "score": {"$meta": "vectorSearchScore"}
            }}
        ]
        return list(self.collection.aggregate(pipeline))

    def get_search_result(self, query: str) -> str:
        """Retrieve formatted search results based on a query"""
        results = self.vector_search(query)
        return "\n\n".join(f"Title: {res['title']}, Plot: {res['fullplot']}" for res in results)
