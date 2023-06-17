from fastapi import APIRouter, Depends, HTTPException
# from sys import Path
from dependencies import get_token_header
from numpy import linspace
from pydantic import BaseModel

# Following info should move to DB or configuration file.
DB_PATH = r".\tests\pyqum.sqlite"

router = APIRouter(
    prefix="/searching",
    # tags=["myapp"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

class Sample(BaseModel):
    id: str
    name: str | None = None

from DB.SQLite_parser import read_sql_lab

@router.get("/samples", tags=["searching"], response_model=list[Sample])
async def get_samples( name: str | None = None ) -> dict:

    mySQL = read_sql_lab(DB_PATH)
    sample_num = len(mySQL.list_samplename())
    samples = []
    for i, n in enumerate(mySQL.update_list_samplename(name)):
        sample_info = {
            "id": i,
            "name": n
        }
        samples.append(sample_info)
    return samples