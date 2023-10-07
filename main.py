from fastapi import FastAPI

from view import router

app = FastAPI(title="Test")


app.include_router(router)
