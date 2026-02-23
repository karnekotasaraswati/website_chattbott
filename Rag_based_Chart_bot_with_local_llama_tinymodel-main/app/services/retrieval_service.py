import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DATA_PATH = "data/documents"  # Fallback local directory
MODEL_NAME = "all-MiniLM-L6-v2"

# --- Globals ---
vector_index = None
documents = []  # List of text chunks corresponding to vector indices
embedder = None

def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Warning: SUPABASE_URL or SUPABASE_KEY not set. Skipping Supabase.")
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return None

def load_documents_from_supabase():
    """Fetches documents from Supabase 'documents' table."""
    client = get_supabase_client()
    if not client:
        return []
    
    try:
        # Assuming table 'documents' with a 'content' column
        response = client.table("documents").select("content").execute()
        data = response.data
        if not data:
            print("No documents found in Supabase.")
            return []
        
        texts = [item['content'] for item in data if item.get('content')]
        print(f"Loaded {len(texts)} documents from Supabase.")
        return texts
    except Exception as e:
        print(f"Error fetching from Supabase: {e}")
        return []

def load_local_documents():
    """Loads .txt files from local data directory."""
    texts = []
    if not os.path.exists(DATA_PATH):
        return texts
    
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".txt"):
            path = os.path.join(DATA_PATH, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    texts.append(f.read())
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    print(f"Loaded {len(texts)} local documents.")
    return texts

def create_chunks(texts, chunk_size=500):
    """Splits long texts into smaller chunks for better scaffolding."""
    chunks = []
    for text in texts:
        # Simple splitting by approximate character count
        # In production, use a proper text splitter (e.g., recursive character splitter)
        words = text.split()
        for i in range(0, len(words), 100):  # Overlap could be added here
            chunk = " ".join(words[i:i+200])
            if chunk:
                chunks.append(chunk)
    return chunks

def build_vector_store():
    """Rebuilds the FAISS index from scratch using Supabase + Local files."""
    global vector_index, documents, embedder
    
    print("Initializing embedding model...")
    if embedder is None:
        embedder = SentenceTransformer(MODEL_NAME)
        
    print("Fetching documents...")
    supabase_docs = load_documents_from_supabase()
    local_docs = load_local_documents()
    
    all_docs = supabase_docs + local_docs
    chunks = create_chunks(all_docs)
    
    if not chunks:
        print("No documents to index.")
        vector_index = None
        documents = []
        return

    print(f"Embedding {len(chunks)} chunks...")
    embeddings = embedder.encode(chunks)
    
    # Initialize FAISS
    dimension = embeddings.shape[1]
    vector_index = faiss.IndexFlatL2(dimension)
    vector_index.add(np.array(embeddings).astype('float32'))
    documents = chunks
    
    print(f"Index built with {len(documents)} chunks.")

def load_index():
    """Public API to initialize the service."""
    if vector_index is None:
        build_vector_store()

def refresh_vector_store():
    """Force rebuild of index."""
    build_vector_store()

def search_context(query, k=3):
    """Searches the vector store for relevant context."""
    global vector_index, documents, embedder
    
    if vector_index is None or not documents:
        return ""
    
    if embedder is None:
        load_index()
        
    query_vec = embedder.encode([query])
    distances, indices = vector_index.search(np.array(query_vec).astype('float32'), k)
    
    results = []
    for i in indices[0]:
        if i != -1 and i < len(documents):
            results.append(documents[i])
            
    return "\n\n".join(results)
