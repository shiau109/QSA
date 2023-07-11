from fastapi import APIRouter, Depends, HTTPException
# from sys import Path
from dependencies import get_token_header
from numpy import linspace
from pydantic import BaseModel

# Following info should move to DB or configuration file.
TEST_DB_PATH = r"..\tests\pyqum.sqlite"
TEST_DATA_PATH = r"..\tests"
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
from DB.exp_data.parser.data_praser import ExpDataParser, PyqumPraser
from DB.exp_data.expdata import ExpData

@router.get("/searching/samples", tags=["searching"], response_model=list[Sample])
async def get_samples( name: str | None = None ):

    mySQL = read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)
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

    mySQL = read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)
    sample_num = len(mySQL.list_samplename())
    sample_list = mySQL.update_list_samplename(name)
    return sample_list

@router.get("/sample/{serial_number}", response_model=Sample)
async def get_sample( serial_number: str ) -> dict:

    mySQL = read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)
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
    date: str|None
    comment: str
    configs: dict
    axes: list
    data_labels: list

class JobFilter(BaseModel):
    sn: str
    date: str
    htag:str

class AxisInfo(BaseModel):
    name: str
    position: int

class Plot1DInfo(BaseModel):
    x_axis: dict
    y_axis: dict

@router.get("/job/{job_ID}", tags=["searching"], response_model=JobHeader)
async def get_job( job_ID: str ) -> dict:

    mySQL = read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)
    job_header = mySQL.get_job(job_ID)
    job_data_path = mySQL.jobid_search_pyqum(job_ID)
    parser = PyqumPraser()
    job_data = parser.import_data(job_data_path)
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
        "data_labels": list(job_data.data.keys())
    }
    return job_info

@router.post("/job/{job_ID}/preview1D", tags=["searching"], response_model=Plot1DInfo)
async def get_job_preview1D( job_ID: str, axes_info: list[AxisInfo] ) -> dict:

    mySQL = read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)
    job_header = mySQL.get_job(job_ID)
    job_data_path = mySQL.jobid_search_pyqum(job_ID)
    parser = PyqumPraser()
    job_data = parser.import_data(job_data_path)
    address = [0]*job_data.dimension
    # x_axis_idx = job_data.get_axis_idx( x_axis )
    # data_address[x_axis_idx]=-1
    for a_info in axes_info:
        address_idx = job_data.get_axis_idx( a_info.name )
        print(f"axis {address_idx} {a_info.name} in postion {a_info.position}")
        address[job_data.get_axis_idx( a_info.name )] = a_info.position
    selected_data = job_data.get_subdata(address)
    print(selected_data.get_structure_info())
    x_name = selected_data.exp_vars[0][0]
    plot_info = {
        "x_axis":{
            x_name:selected_data.exp_vars[0][1].tolist(),
        },
        "y_axis":{}
    }
    for name, values in selected_data.data.items():
        plot_info["y_axis"][name] = values.tolist()
    return plot_info

@router.post("/search/job", tags=["searching"], response_model=list[JobHeader])
async def serch_job( filter: JobFilter ) -> list[JobHeader]:

    mySQL = read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)
    selector_d = {
        'id': 'id',
        'sample_id': 'sample',
        'dateday':'date',
        'comment':'comment'
    }
    sampleSN = filter.sn
    dbData = mySQL.filter_job( "sample_id", sampleSN )
    from pandas import DataFrame
    if not isinstance(dbData, type(None)):
        jobs = dbData.rename(columns=selector_d)[selector_d.values()]
        headers = jobs.to_dict('records')
    else:
        headers = []
    return headers