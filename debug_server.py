import uvicorn
import traceback
import sys

try:
    from app.main import app
    if __name__ == "__main__":
        print("Starting debug server...")
        uvicorn.run(app, host="127.0.0.1", port=8000)
except Exception:
    traceback.print_exc()
    sys.exit(1)
