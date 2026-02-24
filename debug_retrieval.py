from app.services.retrieval_service import load_index, search_context

# Initialize services (Supabase + Local + Embeddings + FAISS)
print("Initializing RAG service...")
load_index()

question = "What kind of opportunities best fit my current profile?"
print(f"Searching for: {question}")

context = search_context(question)
print("\n--- Retrieved Context ---")
print(context if context else "No relevant context found.")
print("-------------------------")
