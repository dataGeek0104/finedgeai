from fastapi import FastAPI

# Initialize app globally so uvicorn can discover it
app = FastAPI(title="FinEdgeAI", version="0.0.0")


@app.get("/", description="App information", tags=["Root"])
def health_check():
    return {"name": app.title, "version": app.version, "message": "App is working fine!"}
