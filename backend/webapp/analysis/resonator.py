from fastapi import APIRouter, Depends, HTTPException
# from sys import Path
from dependencies import get_token_header
from pydantic import BaseModel


router = APIRouter(
    prefix="/analysis",
    # tags=["myapp"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

from internal.access import get_db_info


@router.get("/resonator_fit", tags=["analysis"], response_model=str)
async def fit_qFactor( name: str | None = None ):

    mySQL = get_db_info()
    
    return name