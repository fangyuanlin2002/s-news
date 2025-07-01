from fastapi import FastAPI
from app.api import preferences

app = FastAPI(title="S-News API")
@app.get("/")
def root():
    return {"message": "Welcome to S-News API"}

app.include_router(preferences.router, prefix="/preferences", tags=["preferences"])
