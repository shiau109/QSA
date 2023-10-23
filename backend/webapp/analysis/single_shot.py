from fastapi import APIRouter, Depends, HTTPException, FastAPI, Response, BackgroundTasks
# from sys import Path
from dependencies import get_token_header
from pydantic import BaseModel
from pandas import DataFrame
from fastapi.responses import FileResponse
import numpy as np
import pandas as pd

router = APIRouter(
    prefix="/analysis/single_shot",
    # tags=["myapp"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

from internal.access import get_db_info, get_job_expdata
from expData.data_process import PrecessCMD, DataProcesser
from expData.expdata import ExpData
from single_shot.distribution_model import GMM_model



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

@router.post("/state_distinguishability", tags=["single_shot"], response_model=dict)
async def train_model( prePro_req: list[PrecessCMD], ana_req: StateDistCMD ):

    job_data = get_job_expdata( ana_req.jobid )
    data_preProcessor = DataProcesser(job_data)
    new_data = data_preProcessor.import_CMDs(prePro_req)
    report_dict = {}
    match ana_req.model:
        case "GMM":

            training_data = np.array([new_data.get_data("I").flatten(), new_data.get_data("Q").flatten()])
            my_model = GMM_model()
            my_model.import_trainingData(training_data.transpose())

            para_dict = my_model.output_paras()
            report_dict["paras"] = para_dict

            for k, v in para_dict.items():
                para_dict[k] = para_dict[k].tolist()


            data_dict = {
                "I":training_data[0],
                "Q":training_data[1],
                "Label": my_model.get_prediction(training_data.transpose()),
            }
            df = pd.DataFrame( data=data_dict )

            report_dict["data"] = data_dict
            
        case _:
            pass
    return report_dict



from fastapi import File, UploadFile

@router.post('/state_distinguishability/uploadfile')
def upload_file( file: UploadFile ):
    data = np.load(file.file)
    report_dict = {}

    for label in data.keys():
        idata = np.array([])
        qdata = np.array([])
        print(f"{label} with shape {data[label].shape}")
        for i in range(data[label].shape[0]):
            print(idata.shape)
            idata = np.append(idata,data[label][i][0])
            qdata = np.append(qdata,data[label][i][1])
        training_data = np.array([idata, qdata])
        my_model = GMM_model()
        my_model.import_trainingData(training_data.transpose())
    
        para_dict = my_model.output_paras()
        report_dict["paras"] = para_dict
        print(report_dict)
    return {"filename": file.filename}


    


@router.post('/state_distinguishability/plot')
def get_img( prePro_req: list[PrecessCMD], ana_req: StateDistCMD, background_tasks: BackgroundTasks ):
    job_data = get_job_expdata( ana_req.jobid )
    data_preProcessor = DataProcesser(job_data)
    new_data = data_preProcessor.import_CMDs(prePro_req)

    training_data = np.array([new_data.get_data("I").flatten(), new_data.get_data("Q").flatten()])
    my_model = GMM_model()
    my_model.import_trainingData(training_data.transpose())

    para_dict = my_model.output_paras()
    report_dict["paras"] = para_dict

    for k, v in para_dict.items():
        para_dict[k] = para_dict[k].tolist()


    data_dict = {
        "I":training_data[0],
        "Q":training_data[1],
        "Label": my_model.get_prediction(training_data.transpose()),
    }
    df = pd.DataFrame( data=data_dict )

    report_dict["data"] = data_dict

    img_buf = create_img( data_dict )
    background_tasks.add_task(img_buf.close)
    headers = {'Content-Disposition': 'inline; filename="out.png"'}
    return Response(img_buf.getvalue(), headers=headers, media_type='image/png')

    
import io
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt

def create_img( data ):
    plt.rcParams['figure.figsize'] = [7.50, 3.50]
    plt.rcParams['figure.autolayout'] = True
    fig = plt.figure()  # make sure to call this, in order to create a new figure
    plt.plot( data["I"], data["Q"], 'o')
    print(new_data.configs)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    plt.close(fig)
    return img_buf