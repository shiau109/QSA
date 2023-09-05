from fastapi import APIRouter, Depends, HTTPException
# from sys import Path
from dependencies import get_token_header
from numpy import linspace
from pydantic import BaseModel

# Following info should move to DB or configuration file.
# TEST_DB_PATH = r"C:\Users\ASQUM\HODOR\CONFIG\pyqum.sqlite"
# TEST_DATA_PATH = r"C:/Users/ASQUM/HODOR/CONFIG/USRLOG"

router = APIRouter(
    prefix="/sample",
    tags=["sample"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

from internal.access import get_db_info

class SampleDetail(BaseModel):
    id: int
    serialNum: str
    model: str

@router.get("/{serial_number}", response_model=SampleDetail)
async def get_sample_detail( serial_number: str ) -> dict:

    mySQL = get_db_info()
    sample_id = mySQL.select_sample(serial_number)
    sample = {
        "id": sample_id,
        "serialNum": serial_number,
        "model": "prototype"

    }
    return sample