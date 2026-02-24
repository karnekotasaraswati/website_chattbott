import requests
import json
import sys

# Ensure requests is installed or use standard library if unsure, but requests is standard enough.
# If not installed, I'll see an error.

url = "http://127.0.0.1:8000/chat"
headers = {"Content-Type": "application/json"}
data = {"question": "Hi"}

print(f"Sending request to {url}...")
try:
    with requests.post(url, headers=headers, json=data, stream=True) as r:
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Reading stream chunks:")
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    print(f"Created chunk: {len(chunk)} bytes")
                    print(chunk.decode('utf-8', errors='ignore'))
            print("\nStream finished.")
        else:
            print("Error response:", r.text)
except Exception as e:
    print(f"Request failed: {e}")
