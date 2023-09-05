from expData.parser.data_praser import ExpDataParser, PyqumPraser
from expData.expdata import ExpData, DataAddress
from expData.data_process import PrecessCMD, DataProcesser

from typing import TypedDict, Union

from pydantic import BaseModel

class PlotDesination( TypedDict ):
    name:str
    info_type:str
    designation:str

class PlotRequest( BaseModel ):
    type: str
    plot: list[PlotDesination]
    address:list[DataAddress]


class Plot2DBasicReturn(BaseModel):
    trace_name:list[str]
    x: list[float]|list[list[float]]
    y: list[list[float]]

class Plot3DscalarReturn(BaseModel):
    trace_name:list[str]
    x: list[float]
    y: list[float]
    z: list[list[list[float]]]


def plot_data( data:ExpData, plot_request:PlotRequest )->Plot2DBasicReturn:
    print(plot_request)
    match plot_request.type:
        case "2DBasic":
            return plot_2DBasic(data,plot_request)
        case "3DScalar":
            return plot_3Dscalar(data,plot_request)
        case _:
            pass


def plot_2DBasic( data:ExpData, plot_request:PlotRequest )->Plot2DBasicReturn:

    for plot_des in plot_request.plot:
        if plot_des["info_type"] == "var":
            plot_request.address.append({
                "var_name": plot_des["name"],
                "position": [-1],
                "axis": -1,
            })


    selected_data = data.get_subdata(plot_request.address)
    print(selected_data.get_structure_info())
    plot_output = {
        "trace_name":[],
        "x":[selected_data.exp_vars[0][1].tolist()],
        "y":[]
    }
    for plot_des in plot_request.plot:
        if plot_des["designation"] == "y":
            name = plot_des["name"]
            plot_output["trace_name"].append(name)
            plot_output["y"].append(selected_data.data[name].tolist())
    # print(plot_output["y"])
    return plot_output

def plot_3Dscalar( data:ExpData, plot_request:PlotRequest ) -> Plot3DscalarReturn:

    for plot_des in plot_request.plot:
        if plot_des["designation"] == "x":
            print(f"{plot_des['name']} as x")

            plot_request.address.append({
                "var_name": plot_des["name"],
                "position": [-1],
                "axis": -1,
            })
        elif plot_des["designation"] == "y":
            print(f"{plot_des['name']} as y")

            plot_request.address.append({
                "var_name": plot_des["name"],
                "position": [-1],
                "axis": -2,
            })
        elif plot_des["designation"] == "z":
            print(f"{plot_des['name']} as z")

            trace_name = plot_des["name"]
    print(plot_request.address)
    selected_data = data.get_subdata(plot_request.address)
    print(selected_data.get_structure_info())
    plot_output = {
        "trace_name":[trace_name],
        "x":selected_data.exp_vars[0][1].tolist(),
        "y":selected_data.exp_vars[1][1].tolist(),
        "z":[selected_data.get_data(trace_name).tolist()]
    }

    return plot_output
# def plot_DatavsData( plot_info ):


#     address = [0]*job_data.dimension

#     for a_info in pReq.other_position:
#         address_idx = job_data.get_axis_idx( a_info.name )
#         print(f"axis {address_idx} {a_info.name} in postion {a_info.position}")
#         address[address_idx] = a_info.position
#     x_axis_idx = job_data.get_axis_idx( pReq.parameter )
#     address[x_axis_idx]=-1
    
#     print(job_data.get_structure_info(),"New address", address)

#     selected_data = job_data.get_subdata(address)
#     print(selected_data.get_structure_info())
#     plot_info = {
#         "trace_name":[""],
#         "x":[selected_data.data[pReq.x].tolist()],
#         "y":[selected_data.data[pReq.y].tolist()]
#     }