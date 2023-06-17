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

class Hero(BaseModel):
    id: str
    name: str | None = None
from DB.SQLite_parser import read_sql_lab


@router.get("/todo", tags=["mytodos"], response_model=list[Hero])
async def get_todos( name: str | None = None ) -> dict:

    mySQL = read_sql_lab(r".\tests\pyqum.sqlite")
    sample_num = len(mySQL.list_samplename())
    todos = []
    for i, n in enumerate(mySQL.list_samplename()):
        sample_info = {
            "id": i,
            "name": n
        }
        todos.append(sample_info)
    # return { "data": todos }
    return todos