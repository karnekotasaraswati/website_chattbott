# from fastapi import APIRouter
# from pydantic import BaseModel
# from app.services.llm_service import generate_response
#     # from app.services.retrieval_service import search_context

# router = APIRouter()

# class ChatRequest(BaseModel):
#     question: str

# @router.post("/chat")
# async def chat_bot(request: ChatRequest):


#     # context = search_context(request.question)
#     # print("Retrieved Context:", context)

#     prompt = f"""
# You are StarZopp AI Assistant.

# Answer ONLY using this context.
# If answer is not found say: I don't know.

# # Context:
# # {context}

# Question:
# {request.question}
# """

#     answer = generate_response(prompt)
#     print(answer)
#     return {"answer": answer}

# @router.post("/chat")
# async def chat_bot(request: ChatRequest):

#     prompt = f"""
# You are StarZopp AI Assistant.

# Question:
# {request.question}
# """

#     answer = generate_response(prompt)
#     print(answer)

#     return {"answer": answer}


from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.llm_service import generate_response, format_rag_prompt
from app.services.retrieval_service import search_context, DATA_PATH, refresh_vector_store
import os

from app.services.feedback_service import log_interaction, save_feedback
from typing import Optional

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: str   # "success" or "failure"
    reason: Optional[str] = None

@router.post("/feedback")
async def receive_feedback(feedback: FeedbackRequest):
    """
    Receives user feedback (thumbs up/down) and logs it.
    """
    save_feedback(feedback.question, feedback.answer, feedback.rating, feedback.reason)
    return {"status": "Feedback received"}

@router.post("/chat")
async def chat_bot(request: ChatRequest):

    # 1. Simple Greeting Check
    greetings = ["hi", "hello", "hey", "greetings", "hi there", "hello there", "hii", "hola"]
    if request.question.strip().lower() in greetings:
        async def greeting_generator():
            full_response = "Hello! I am StarZopp AI. How can I help you with your career or job search today?"
            yield full_response
            # Log greeting as well
            log_interaction(request.question, full_response)
            
        return StreamingResponse(greeting_generator(), media_type="text/plain")

    # 2. Context retrieval using FAISS
    context = search_context(request.question)
    
    print(f"DEBUG: Retrieved Context for '{request.question}':\n{context[:200]}...\n---\n")

    # Format Prompt
    prompt = format_rag_prompt(request.question, context)

    print("DEBUG: Generating LLM response...")
    
    # Wrapper to log the full response after streaming
    async def logging_wrapper(generator):
        full_response = ""
        async for chunk in generator:
            full_response += chunk
            yield chunk
        
        # Log the completed interaction
        log_interaction(request.question, full_response)

    # Return streaming response
    return StreamingResponse(logging_wrapper(generate_response(prompt)), media_type="text/plain")


@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """Upload a new knowledge document (PDF or TXT) and refresh the vector store.

    This saves the file under data/documents/ and rebuilds the FAISS index so
    future /chat calls can use the new content.
    """
    filename = file.filename or ""
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext not in {".txt", ".pdf"}:
        raise HTTPException(status_code=400, detail="Only .txt and .pdf files are supported")

    os.makedirs(DATA_PATH, exist_ok=True)
    dest_path = os.path.join(DATA_PATH, filename)

    contents = await file.read()
    with open(dest_path, "wb") as f:
        f.write(contents)

    # Rebuild vector DB so the new file is included in RAG
    refresh_vector_store()

    return {"message": "Document uploaded and knowledge index refreshed", "filename": filename}
