from fastapi import FastAPI

app = FastAPI(title="API Key Service")


@app.get("/health")
def health():
    return {"status": "ok"}