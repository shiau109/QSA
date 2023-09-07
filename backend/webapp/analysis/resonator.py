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

from internal.access import get_db_info, get_job_expdata
from expData.data_process import PrecessCMD, DataProcesser


class analysisCMD( BaseModel ):
    configs: dict
    axes: list
    data_labels: list[str]

class ResonatorFitCMD( BaseModel ):
    jobid: str
    model: str
    freq_axis: str
    

@router.post("/resonator_fit", tags=["analysis"], response_model=str)
async def fit_qFactor( prePro_req: list[PrecessCMD], ana_req: ResonatorFitCMD ):

    job_data = get_job_expdata( ana_req.jobid )
    data_preProcessor = DataProcesser(job_data)
    new_data = data_preProcessor.import_CMDs(prePro_req)

    return name