import httpx
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"

def format_rag_prompt(query: str, context: str) -> str:
    """Formats the prompt for generate_response."""
    prompt = f"""<|system|>
You are a helpful AI assistant. Use the following context to answer the user's question. If the answer is not in the context, say "I don't know".
Context:
{context}
</s>
<|user|>
{query}
</s>
<|assistant|>"""
    return prompt

async def generate_response(prompt: str):
    """
    Generate a streaming response from Ollama.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.1,  # Low temperature for factual RAG
            "num_ctx": 2048       # Context window
        }
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", OLLAMA_URL, json=payload) as response:
                if response.status_code != 200:
                    yield f"Error: Ollama service returned {response.status_code}"
                    return

                async for chunk in response.aiter_lines():
                    if chunk:
                        try:
                            item = json.loads(chunk)
                            if "response" in item:
                                yield item["response"]
                            if item.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue
    except Exception as e:
        yield f"Error connecting to Ollama: {str(e)}"
