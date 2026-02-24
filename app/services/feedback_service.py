import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

FEEDBACK_FILE = "data/feedback_logs.jsonl"
CHAT_LOGS_FILE = "data/chat_logs.jsonl"

def append_to_jsonl(file_path: str, data: dict):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        data["timestamp"] = datetime.now().isoformat()
        f.write(json.dumps(data) + "\n")

def log_interaction(question: str, answer: str):
    """Logs the raw interaction as a default 'success' or just a record."""
    data = {
        "event": "chat_completion",
        "question": question,
        "answer": answer
    }
    append_to_jsonl(CHAT_LOGS_FILE, data)

def save_feedback(question: str, answer: str, rating: str, reason: Optional[str] = None):
    """Logs the user feedback."""
    data = {
        "event": "user_feedback",
        "question": question,
        "answer": answer,
        "rating": rating,
        "reason": reason
    }
    append_to_jsonl(FEEDBACK_FILE, data)
