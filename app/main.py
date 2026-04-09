from fastapi import FastAPI
from fastapi.security import HTTPBearer

from app.api.routes import router
from app.db.session import engine
from app.db.base import Base
from app.models import user

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API Key Service"
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
