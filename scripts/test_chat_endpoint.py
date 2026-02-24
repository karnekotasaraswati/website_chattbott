import urllib.request
import json

def test_query(question):
    url = "http://127.0.0.1:8000/chat"
    data = json.dumps({"question": question}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Question: {question}")
            print(f"Response: {response.read().decode('utf-8')}")
            print("-" * 20)
    except Exception as e:
        print(f"Error for '{question}': {e}")

if __name__ == "__main__":
    print("Testing Greeting:")
    test_query("Hi")
    
    print("\nTesting Greeting (mixed case):")
    test_query("HeLLo")
    
    print("\nTesting RAG Question:")
    test_query("What are the benefits of premium plan?")
