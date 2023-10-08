from fastapi import FastAPI

from app.view import router

app = FastAPI(title="Test")


app.include_router(router)
