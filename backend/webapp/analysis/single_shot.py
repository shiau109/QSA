from fastapi import APIRouter, Depends, HTTPException
# from sys import Path
from dependencies import get_token_header
from pydantic import BaseModel

from expData.expdata import ExpData
import numpy as np

router = APIRouter(
    prefix="/analysis/single_shot",
    # tags=["myapp"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

from internal.access import get_db_info, get_job_expdata
from expData.data_process import PrecessCMD, DataProcesser
from pandas import DataFrame
from fastapi.responses import FileResponse

# class analysisCMD( BaseModel ):
#     configs: dict
#     axes: list
#     data_labels: list[str]

class StateDistCMD( BaseModel ):
    jobid: str
    model: str
    shot_axis: str

# from pathlib import Path

download_folder = r"download_temp/"
state_dist_fn = r"state_dist.npz"

from single_shot.distribution_model import GMM_model
@router.post("/state_distinguishability", tags=["single_shot"], response_model=dict)
async def train_model( prePro_req: list[PrecessCMD], ana_req: StateDistCMD ):

    job_data = get_job_expdata( ana_req.jobid )
    data_preProcessor = DataProcesser(job_data)
    new_data = data_preProcessor.import_CMDs(prePro_req)
    para_dict = {}
    match ana_req.model:
        case "GMM":
            training_data = np.array([new_data.get_data("I").flatten(), new_data.get_data("Q").flatten()])
            my_model = GMM_model()
            my_model.training(training_data.transpose())
            para_dict = my_model.output_paras()
            print(para_dict)
            for k, v in para_dict.items():
                para_dict[k] = para_dict[k].tolist()
            print(para_dict)

        case _:
            pass


    return para_dict
