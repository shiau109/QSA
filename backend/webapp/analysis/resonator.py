from fastapi import APIRouter, Depends, HTTPException
# from sys import Path
from dependencies import get_token_header
from pydantic import BaseModel

from expData.expdata import ExpData
from numpy import ndarray, linspace

router = APIRouter(
    prefix="/analysis",
    # tags=["myapp"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

from internal.access import get_db_info, get_job_expdata
from expData.data_process import PrecessCMD, DataProcesser
from pandas import DataFrame

class analysisCMD( BaseModel ):
    configs: dict
    axes: list
    data_labels: list[str]

class ResonatorFitCMD( BaseModel ):
    jobid: str
    model: str
    freq_axis: str
    # power_axis: str
    
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

            para_dict = df_fitParas.to_dict("list")
            fit_num = len(df_fitParas.index)
            para_dict["index"] = linspace(0,fit_num-1,fit_num, dtype=int).tolist()

            print(para_dict.keys())

        case _:
            pass
    return para_dict



def notch_complex_fit( data:ndarray ):

    s21 = data
    freq *=1e9
    seleted_power = []
    for p in input_power.tolist():
        if p < VNA_minpower:
            seleted_power.append(p)
        else:
            seleted_power.append(VNA_minpower)
    power_mk = input_power-attenuation
    part_result, fitCurves = cavityQ_fit_dependency(freq, s21, power=power_mk)
    powerQ_results.append( part_result )
    part_raw_dfs = mat_to_df( f"{raw_data_fd}/{fn}.mat" )
    raw_dfs.extend(part_raw_dfs)
    # plot_cavityS21_fitting( freq, s21, fitCurves, input_power, title=fn )
    plot_cavityS21_fitting( freq, s21, fitCurves, input_power, title=fn, output_fd=power_dep_folder )

