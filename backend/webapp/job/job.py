from fastapi import APIRouter, Depends, HTTPException
# from sys import Path
from dependencies import get_token_header
from numpy import linspace 
from pydantic import BaseModel

# Following info should move to DB or configuration file.

router = APIRouter(
    prefix="/job",
    tags=["job"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)



from internal.access import get_db_info, get_job_header, get_job_expdata
from expData.data_process import PrecessCMD, DataProcesser






class JobHeader(BaseModel):
    id: str
    sample: str
    date: str|None
    comment: str
    configs: dict
    axes: list
    data_labels: list


class ExpData_Info( BaseModel ):
    configs: dict
    axes: list
    data_labels: list[str]

from .data_plot import PlotRequest, plot_data, Plot2DBasicReturn, Plot3DscalarReturn
from fastapi.responses import FileResponse


@router.get("/{job_ID}", response_model=JobHeader)
async def get_job( job_ID: str ) -> dict:

    job_header = get_job_header( job_ID )
    job_data = get_job_expdata( job_ID )
    axis_infos = []
    for exp_var in job_data.exp_vars:
        axis_info = (exp_var[0],len(exp_var[1]))
        axis_infos.append(axis_info)
    # print(job)
    # print(job["task"].values[0])
    job_info = {
        "id": str(job_header["id"].values[0]),
        "sample": str(job_header["sample_id"].values[0]),
        "date": str(job_header["dateday"].values[0]),
        "comment": str(job_header["comment"].values[0]),
        "configs": job_data.configs,
        "axes": axis_infos,
        "data_labels": list(job_data.data.keys()),
    }
    return job_info

@router.post("/{job_ID}/preprocess", response_model=ExpData_Info)
async def get_job_preprocess( job_ID: str, prePro_req: list[PrecessCMD] ) -> ExpData_Info:
    
    job_data = get_job_expdata( job_ID )
    data_preProcessor = DataProcesser(job_data)
    new_data = data_preProcessor.import_CMDs(prePro_req)
    axis_infos = []
    for exp_var in job_data.exp_vars:
        axis_info = (exp_var[0],len(exp_var[1]))
        axis_infos.append(axis_info)
    data_info = {
        "configs": new_data.configs,
        "axes": list(axis_infos),
        "data_labels": list(new_data.data.keys()),
    }
    print(data_info)
    return data_info

@router.post("/{job_ID}/preview", response_model=Plot2DBasicReturn|Plot3DscalarReturn)
async def get_job_preview( job_ID: str, polt_req: PlotRequest, prePro_req: list[PrecessCMD] ) -> dict:
    job_data = get_job_expdata( job_ID )
    # Pre process
    data_preProcessor = DataProcesser(job_data)
    new_data = data_preProcessor.import_CMDs(prePro_req)

    plot_package = plot_data(new_data, polt_req)
    return plot_package

@router.post("/{job_ID}/download/rawdata", response_class=FileResponse)
async def get_download_rawdata( job_ID: str ) -> dict:
    db_info = get_db_info()

    from pathlib import Path

    rawdata_path = Path(db_info.jobid_search_pyqum( job_ID ))
    print(f"Download raw data with jobID {job_ID} from {rawdata_path}")

    # path = Path(rawdata_path)
    if "pyqum" in rawdata_path.suffix:
        filename = f"{job_ID}.pyqum"
    else:  
        filename = job_ID+rawdata_path.suffix
    return FileResponse(rawdata_path, filename=filename)
