# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.chat import router

# app = FastAPI()

# # ✅ ENABLE CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],   # allow all (for development)
#     allow_credentials=True,
#     allow_methods=["*"],   # allow POST, OPTIONS, GET
#     allow_headers=["*"],
# )

# app.include_router(router)

# @app.get("/")
# def home():
#     return {"status": "AI Chatbot Running"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.api.chat import router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register API router
app.include_router(router)


# ✅ SAFE STARTUP EVENT
@app.on_event("startup")
async def startup_event():
    print("🚀 Application Startup: Connecting to Services...")

    try:
        from app.services.retrieval_service import load_index
        load_index()
        print("✅ FAISS index loaded")
    except Exception as e:
        print("❌ ERROR during startup:", e)
        print("⚠️ Server will continue without RAG")


# ✅ Frontend path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_PATH = os.path.join(BASE_DIR, "..", "index.html")


@app.get("/")
def serve_frontend():
    if os.path.exists(FRONTEND_PATH):
        return FileResponse(FRONTEND_PATH)
    return {"message": "API is running 🚀"}