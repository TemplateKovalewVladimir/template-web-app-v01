"""test"""
from decimal import Decimal

from fastapi import APIRouter

router = APIRouter(prefix="/test", tags=["test"])


@router.get("")
def hello():
    return {
        "test": Decimal(123),
    }
