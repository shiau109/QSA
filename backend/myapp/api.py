from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_token_header

router = APIRouter(
    prefix="/myapp",
    tags=["myapp"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


todos = [
    {
        "id": "1",
        "item": "A"
    },
    {
        "id": "2",
        "item": "B"
    },
    {
        "id": "3",
        "item": "C"
    },
    {
        "id": "4",
        "item": "D"
    }
]



@router.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return { "data": todos }