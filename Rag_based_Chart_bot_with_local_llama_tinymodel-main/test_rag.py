import requests
import json

url = "http://127.0.0.1:8000/chat"
headers = {"Content-Type": "application/json"}

def test_chat(question):
    data = {"question": question}
    print(f"\n--- Asking: {question} ---")
    try:
        with requests.post(url, headers=headers, json=data, stream=True) as r:
            if r.status_code == 200:
                print("Response:")
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        print(chunk.decode('utf-8', errors='ignore'), end='', flush=True)
                print("\n")
            else:
                print("Error:", r.text)
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    # Test Greeting
    test_chat("Hello")
    
    # Test RAG - Account Types
    test_chat("What are the different account types available?")

    # Test RAG - Job System
    test_chat("How does the job system work?")
    
    # Test RAG - Collaboration
    test_chat("Tell me about collaboration events.")
