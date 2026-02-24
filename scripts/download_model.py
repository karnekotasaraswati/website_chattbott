import os
import sys
import requests

# URL for TinyLlama GGUF (smaller, faster than Phi-2)
MODEL_URL = "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

def download_model():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        print(f"Created directory: {MODEL_DIR}")

    # Check if file exists and get its size
    file_size = os.path.getsize(MODEL_PATH) if os.path.exists(MODEL_PATH) else 0
    
    # Send HEAD request to get total size
    try:
        print(f"Checking model at: {MODEL_URL}")
        head_resp = requests.head(MODEL_URL, allow_redirects=True)
        total_size = int(head_resp.headers.get('content-length', 0))
    except Exception as e:
        print(f"Failed to fetch model info: {e}")
        return

    if total_size > 0 and file_size == total_size:
        print(f"Model already downloaded and verified: {MODEL_PATH}")
        return

    if total_size > 0 and file_size > total_size:
        print("Existing file is larger than expected. Deleting and restarting.")
        os.remove(MODEL_PATH)
        file_size = 0

    print(f"Downloading Phi-2 model to {MODEL_PATH}...")
    print(f"Source: {MODEL_URL}")
    print(f"Total size: {total_size / (1024*1024):.2f} MB")
    
    headers = {"Range": f"bytes={file_size}-"} if file_size > 0 else {}
    mode = 'ab' if file_size > 0 else 'wb'

    if file_size > 0:
        print(f"Resuming download from {file_size / (1024*1024):.2f} MB...")

    try:
        with requests.get(MODEL_URL, headers=headers, stream=True, allow_redirects=True) as r:
            r.raise_for_status()
            with open(MODEL_PATH, mode) as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk:
                        f.write(chunk)
                        file_size += len(chunk)
                        
                        # Progress bar
                        if total_size > 0:
                            percent = (file_size / total_size) * 100
                            sys.stdout.write(f"\rProgress: {percent:.2f}% ({file_size / (1024*1024):.2f} MB)")
                            sys.stdout.flush()
                        else:
                             sys.stdout.write(f"\rDownloaded: {file_size / (1024*1024):.2f} MB")
                             sys.stdout.flush()

        print("\nDownload complete!")
    except Exception as e:
        print(f"\nError downloading model: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    download_model()
