from fastapi import APIRouter, Depends, HTTPException
# from sys import Path
from dependencies import get_token_header
from numpy import linspace
from pydantic import BaseModel

router = APIRouter(
    prefix="/myapp",
    # tags=["myapp"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

