from fastapi import APIRouter, Depends, HTTPException
# from sys import Path
from dependencies import get_token_header
from numpy import linspace
from pydantic import BaseModel

# Following info should move to DB or configuration file.
DB_PATH = r".\tests\pyqum.sqlite"

router = APIRouter(
    # prefix="/searching",
    # tags=["myapp"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

class Sample(BaseModel):
    id: int
    serialNum: str
    model: str

from DB.SQLite_parser import read_sql_lab

@router.get("/searching/samples", tags=["searching"], response_model=list[Sample])
async def get_samples( name: str | None = None ):

    mySQL = read_sql_lab(DB_PATH)
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

@router.get("/searching/sample-list", tags=["searching"], response_model=list[str])
async def get_samples( name: str | None = None ):

    mySQL = read_sql_lab(DB_PATH)
    sample_num = len(mySQL.list_samplename())
    sample_list = mySQL.update_list_samplename(name)
    return sample_list

@router.get("/sample/{serial_number}", response_model=Sample)
async def get_sample( serial_number: str ) -> dict:

    mySQL = read_sql_lab(DB_PATH)
    sample_id = mySQL.select_sample(serial_number)
    sample = {
        "id": sample_id,
        "serialNum": serial_number,
        "model": "prototype"

    }
    return sample

class JobHeader(BaseModel):
    id: str
    sample: str
    date:str
    comment: str

class JobFilter(BaseModel):
    sn: str
    date: str
    htag:str
  
# @router.get("/job", tags=["searching"], response_model=list[JobHeader])
# async def get_jobs( name: str | None = None ):

#     mySQL = read_sql_lab(DB_PATH)
#     sample_num = len(mySQL.list_samplename())
#     samples = []
#     for i, sn in enumerate(mySQL.update_list_samplename(name)):
#         sample_info = {
#             "id": i,
#             "serialNum": sn,
#             "model": "prototype"
#         }
#         samples.append(sample_info)
#     return samples

@router.get("/job/{job_ID}", tags=["searching"], response_model=JobHeader)
async def get_job( job_ID: str ) -> dict:

    mySQL = read_sql_lab(DB_PATH)
    job = mySQL.get_job(job_ID)
    print(type(job))
    # print(job)
    # print(job["task"].values[0])
    job_header = {
        "id": str(job["id"].values[0]),
        "sample": str(job["sample_id"].values[0]),
        "date": str(job["dateday"].values[0]),
        "comment": str(job["comment"].values[0]),
    }
    return job_header

@router.post("/search/job", tags=["searching"], response_model=list[JobHeader])
async def serch_job( filter: JobFilter ) -> list[JobHeader]:

    mySQL = read_sql_lab(DB_PATH)
    selector_d = {
        'id': 'id',
        'sample_id': 'sample',
        'dateday':'date',
        'comment':'comment'
    }
    sampleSN = filter.sn
    dbData = mySQL.filter_job( "sample_id", sampleSN )
    print(dbData)
    from pandas import DataFrame
    if not isinstance(dbData, type(None)):
        jobs = dbData.rename(columns=selector_d)[selector_d.values()]
        headers = jobs.to_dict('records')
    else:
        headers = []
    return headers