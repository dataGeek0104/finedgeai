import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("CLI_PORT", 8000))  # default to 8000 if not set
    uvicorn.run("app.app:app", host="localhost", port=port, reload=True)
