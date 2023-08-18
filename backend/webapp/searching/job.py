from fastapi import APIRouter, Depends, HTTPException
# from sys import Path
from dependencies import get_token_header
from numpy import linspace
from pydantic import BaseModel

# Following info should move to DB or configuration file.
TEST_DB_PATH = r"C:\Users\ASQUM\HODOR\CONFIG\pyqum.sqlite"
TEST_DATA_PATH = r"C:/Users/ASQUM/HODOR/CONFIG/USRLOG"
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
from DB.exp_data.data_process import PrecessCMD, DataProcesser


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


class JobSummary(BaseModel):
    id: str
    note: str    

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

class ExpDataAxes(BaseModel):
    name: str
    position: int

class PlotDataInfo(BaseModel):
    name: str
    axis: str

class PlotRequest(BaseModel):
    shape: list[ExpDataAxes]
    axies_info: list[PlotDataInfo]

class Plot1DReturn(BaseModel):
    trace_name:list[str]
    x: list[list[float]]
    y: list[list[float]]

class PlotContourReturn(BaseModel):
    trace_name:list[str]
    x: list[float]
    y: list[float]
    z: list[list[list[float]]]

class Plot1DFuncRequest(BaseModel):
    x: str
    y: list[str]
    other_position:list[ExpDataAxes]

class PlotParEqRequest(BaseModel):
    x: str
    y: str
    parameter: str
    other_position:list[ExpDataAxes]

class PlotContourRequest(BaseModel):
    x: str
    y: str
    z: list[str]
    other_position:list[ExpDataAxes]

class ExpData_Info( BaseModel ):
    configs: dict
    axes: list
    data_labels: list[str]

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
        "data_labels": list(job_data.data.keys()),
    }
    return job_info

@router.post("/job/{job_ID}/preprocess", tags=["searching"], response_model=ExpData_Info)
async def get_job_preprocess( job_ID: str, pProReq: list[PrecessCMD] ) -> ExpData_Info:
    print(job_ID,pProReq)
    mySQL = read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)
    job_data_path = mySQL.jobid_search_pyqum(job_ID)
    parser = PyqumPraser()
    job_data = parser.import_data(job_data_path)
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


@router.post("/job/{job_ID}/preview1D", tags=["searching"], response_model=Plot1DReturn)
async def get_job_preview1D( job_ID: str, pReq: Plot1DFuncRequest, pProReq: list[PrecessCMD] ) -> dict:
    print(job_ID,pReq,pProReq)
    mySQL = read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)
    job_data_path = mySQL.jobid_search_pyqum(job_ID)
    parser = PyqumPraser()
    job_data = parser.import_data(job_data_path)
    # Pre process
    data_preProcessor = DataProcesser(job_data)
    new_data = data_preProcessor.import_CMDs(pProReq)

    address = [0]*new_data.dimension

    for a_info in pReq.other_position:
        address_idx = new_data.get_axis_idx( a_info.name )
        print(f"axis {address_idx} {a_info.name} in postion {a_info.position}")
        address[address_idx] = a_info.position
    x_axis_idx = new_data.get_axis_idx( pReq.x )
    address[x_axis_idx]=-1

    selected_data = new_data.get_subdata(address)
    print(selected_data.get_structure_info())
    plot_info = {
        "trace_name":[],
        "x":[selected_data.exp_vars[0][1].tolist()],
        "y":[]
    }
    for name in pReq.y:
        plot_info["trace_name"].append(name)
        plot_info["y"].append(selected_data.data[name].tolist())
    return plot_info

@router.post("/job/{job_ID}/previewParEq", tags=["searching"], response_model=Plot1DReturn)
async def get_job_previewParEq( job_ID: str, pReq: PlotParEqRequest ) -> dict:

    mySQL = read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)
    job_data_path = mySQL.jobid_search_pyqum(job_ID)
    parser = PyqumPraser()
    job_data = parser.import_data(job_data_path)
    address = [0]*job_data.dimension

    for a_info in pReq.other_position:
        address_idx = job_data.get_axis_idx( a_info.name )
        print(f"axis {address_idx} {a_info.name} in postion {a_info.position}")
        address[address_idx] = a_info.position
    x_axis_idx = job_data.get_axis_idx( pReq.parameter )
    address[x_axis_idx]=-1
    
    print(job_data.get_structure_info(),"New address", address)

    selected_data = job_data.get_subdata(address)
    print(selected_data.get_structure_info())
    plot_info = {
        "trace_name":[""],
        "x":[selected_data.data[pReq.x].tolist()],
        "y":[selected_data.data[pReq.y].tolist()]
    }
    return plot_info


@router.post("/job/{job_ID}/previewContour", tags=["searching"], response_model=PlotContourReturn)
async def get_job_previewContour( job_ID: str, pReq: PlotContourRequest ) -> dict:

    mySQL = read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)
    job_data_path = mySQL.jobid_search_pyqum(job_ID)
    parser = PyqumPraser()
    job_data = parser.import_data(job_data_path)
    address = [0]*job_data.dimension

    for a_info in pReq.other_position:
        address_idx = job_data.get_axis_idx( a_info.name )
        print(f"axis {address_idx} {a_info.name} in postion {a_info.position}")
        address[address_idx] = a_info.position
    x_axis_idx = job_data.get_axis_idx( pReq.x )
    y_axis_idx = job_data.get_axis_idx( pReq.y )

    address[x_axis_idx]=-1
    address[y_axis_idx]=-1

    print(job_data.get_structure_info(),"New address", address)

    selected_data = job_data.get_subdata(address)
    
    selected_data.resturcture((selected_data.get_axis_idx( pReq.x ),selected_data.get_axis_idx( pReq.y )))
    print(selected_data.get_structure_info())
    plot_info = {
        "trace_name":[],
        "x":selected_data.exp_vars[0][1].tolist(),
        "y":selected_data.exp_vars[1][1].tolist(),
        "z":[]
    }

    for name in pReq.z:
        plot_info["trace_name"].append(name)
        plot_info["z"].append(selected_data.data[name].tolist())
    return plot_info



@router.post("/search/job", tags=["searching"], response_model=list[JobSummary])
async def serch_job( filter: JobFilter ) -> list[JobSummary]:

    mySQL = read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)
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