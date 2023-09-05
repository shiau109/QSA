from fastapi import APIRouter, Depends, HTTPException
# from sys import Path
from dependencies import get_token_header
from numpy import linspace
from pydantic import BaseModel

from internal.access import get_dataInfo

router = APIRouter(
    prefix="/searching",
    tags=["searching"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)



class JobFilter(BaseModel):
    sn: str
    date: str
    htag:str

class JobSummary(BaseModel):
    id: str
    note: str    

@router.post("/job", response_model=list[JobSummary])
async def search_job( filter: JobFilter ) -> list[JobSummary]:

    mySQL = get_dataInfo()
    selector_d = {
        'id': 'id',
        'note': 'note',
    }
    sampleSN = filter.sn
    dbData = mySQL.filter_job( "sample_id", sampleSN )
    # from pandas import DataFrame
    if not isinstance(dbData, type(None)):
        jobs = dbData.rename(columns=selector_d)[selector_d.values()]
        summaries = jobs.to_dict('records')
    else:
        summaries = []
    return summaries


class SampleIntro(BaseModel):
    id: int
    serialNum: str
    model: str

@router.get("/samples", response_model=list[SampleIntro])
async def get_samples( name: str | None = None ):

    mySQL = get_dataInfo()
    sample_num = len(mySQL.list_samplename())
    samples = []
    for i, sn in enumerate(mySQL.update_list_samplename(name)):
        sample_info = {
            "id": i,
            "serialNum": sn,
            "model": "prototype"
        }
        samples.append(sample_info)
    return samples

@router.get("/sample-list", response_model=list[str])
async def get_samples( name: str | None = None ):

    mySQL = get_dataInfo()
    sample_num = len(mySQL.list_samplename())
    sample_list = mySQL.update_list_samplename(name)
    return sample_list
