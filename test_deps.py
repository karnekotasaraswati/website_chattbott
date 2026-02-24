
print("Testing dependencies...")
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
print("Imports successful.")

load_dotenv()
print(f"Supabase URL: {os.getenv('SUPABASE_URL')}")

print("Loading SentenceTransformer...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded.")

print("Testing embedding...")
vec = model.encode(["hello world"])
print(f"Embedding shape: {vec.shape}")
print("Test complete.")
