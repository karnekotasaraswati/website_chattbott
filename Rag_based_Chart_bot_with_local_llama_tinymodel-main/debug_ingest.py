from app.services.retrieval_service import refresh_vector_store
import traceback

try:
    print("Starting refresh...")
    refresh_vector_store()
    print("Refresh complete.")
except Exception:
    traceback.print_exc()
