from fastapi import APIRouter, Depends, HTTPException
# from sys import Path
from dependencies import get_token_header
from pydantic import BaseModel

from expData.expdata import ExpData
import numpy as np

router = APIRouter(
    prefix="/analysis",
    # tags=["myapp"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

from internal.access import get_db_info, get_job_expdata
from expData.data_process import PrecessCMD, DataProcesser
from pandas import DataFrame
from fastapi.responses import FileResponse

class analysisCMD( BaseModel ):
    configs: dict
    axes: list
    data_labels: list[str]

class ResonatorFitCMD( BaseModel ):
    jobid: str
    model: str
    freq_axis: str
    # power_axis: str


# from pathlib import Path

download_folder = r"download_temp/"
resonator_fit_fn = r"resonator_fit.npz"

from .resonator_analysis_method import cavityQ_fit
@router.post("/resonator_fit", tags=["analysis"], response_model=dict)
async def fit_qFactor( prePro_req: list[PrecessCMD], ana_req: ResonatorFitCMD ):

    job_data = get_job_expdata( ana_req.jobid )
    data_preProcessor = DataProcesser(job_data)
    new_data = data_preProcessor.import_CMDs(prePro_req)
    para_dict = {}
    match ana_req.model:
        case "notch":
            s21 = new_data.get_data("I")+1j*new_data.get_data("Q")
            freq = new_data.get_var_vals( ana_req.freq_axis ) 
            df_fitParas, fitCurves = cavityQ_fit(freq, s21)

            fit_num = len(df_fitParas.index)
            df_fitParas["index"] = np.linspace(0,fit_num-1,fit_num, dtype=int)
            
            para_dict = df_fitParas.to_dict("list")

            # print(df_fitParas.to_numpy())
            np.savez(download_folder+resonator_fit_fn, **para_dict)

        case _:
            pass
    return para_dict


@router.post("/resonator_fit/download", tags=["analysis"], response_class=FileResponse)
async def download_qFactor() -> dict:

    print(f"Download resonator fit result from {download_folder+resonator_fit_fn}")
    data_path = download_folder+resonator_fit_fn
    return FileResponse(data_path, filename=resonator_fit_fn)



# def notch_complex_fit( data:ndarray ):

#     s21 = data
#     freq *=1e9
#     seleted_power = []
#     for p in input_power.tolist():
#         if p < VNA_minpower:
#             seleted_power.append(p)
#         else:
#             seleted_power.append(VNA_minpower)
#     power_mk = input_power-attenuation
#     part_result, fitCurves = cavityQ_fit_dependency(freq, s21, power=power_mk)
#     powerQ_results.append( part_result )
#     part_raw_dfs = mat_to_df( f"{raw_data_fd}/{fn}.mat" )
#     raw_dfs.extend(part_raw_dfs)
#     # plot_cavityS21_fitting( freq, s21, fitCurves, input_power, title=fn )
#     plot_cavityS21_fitting( freq, s21, fitCurves, input_power, title=fn, output_fd=power_dep_folder )

