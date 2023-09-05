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




from internal.access import get_job_header, get_job_expdata
from expData.data_process import PrecessCMD, DataProcesser






class JobHeader(BaseModel):
    id: str
    sample: str
    date: str|None
    comment: str
    configs: dict
    axes: list
    data_labels: list


class PlotDataInfo(BaseModel):
    name: str
    axis: str


class Plot1DReturn(BaseModel):
    trace_name:list[str]
    x: list[list[float]]
    y: list[list[float]]



class ExpData_Info( BaseModel ):
    configs: dict
    axes: list
    data_labels: list[str]

from .data_plot import PlotRequest, plot_data, Plot2DBasicReturn, Plot3DscalarReturn


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
async def get_job_preprocess( job_ID: str, pProReq: list[PrecessCMD] ) -> ExpData_Info:
    
    job_data = get_job_expdata( job_ID )
    data_preProcessor = DataProcesser(job_data)
    new_data = data_preProcessor.import_CMDs(pProReq)
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
async def get_job_preview( job_ID: str, pReq: PlotRequest, pProReq: list[PrecessCMD] ) -> dict:
    print(job_ID,pReq,pProReq)
    job_data = get_job_expdata( job_ID )
    # Pre process
    data_preProcessor = DataProcesser(job_data)
    new_data = data_preProcessor.import_CMDs(pProReq)

    plot_package = plot_data(new_data, pReq)
    return plot_package


