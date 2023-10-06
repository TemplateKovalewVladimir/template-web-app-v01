from fastapi import FastAPI
from decimal import Decimal


app = FastAPI(
    title='Test'
)


@app.get('/')
def hello():
    return {"test": Decimal(123)}
