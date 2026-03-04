from fastapi import FastAPI
"""main docstring"""

app = FastAPI()

@app.get("/health")
def health():
    """Used to check the health of the application"""
    return {"status": "ok"}

