from .expdata import ExpData
from pydantic import BaseModel
import numpy as np

class PrecessCMD(BaseModel):
    method: str
    target: list[str]
    parameter: dict
    output: list[str]

class DataProcesser:
    def __init__( self, data:ExpData ):
        self.expdata = data

    def import_CMDs( self, cmds:list[PrecessCMD])->ExpData:
        for cmd in cmds:
            self.__cmd_parser(cmd)
        return self.expdata
    
    def __cmd_parser( self, cmd ):
        match cmd.method:
            case "mean":
                self.mean( cmd.target, cmd.parameter["axis"], cmd.parameter["range"] )
            case "complex":
                name_re = cmd.target[0]
                name_im = cmd.target[1]
                self.to_complex( name_re, name_im, cmd.output[0] )
            case "abs":
                self.get_abs( cmd.target, cmd.output )
            case "angle":
                self.get_angle( cmd.target, cmd.output )
            case _:
                print(f"No {cmd} method.")
        
    def mean( self, targets:list[str], axis:str, idx_range:tuple[int,int]=None )->ExpData:

        mean_ax = self.expdata.get_axis_idx(axis)
        output_data = {}

        if mean_ax != None:
            
            axis_len = self.expdata.get_structure_info()[mean_ax][1]
            filter_int = np.arange(axis_len)
            bool_filter = np.zeros(axis_len,dtype=bool)
            bool_filter[(filter_int > idx_range[0]) | (filter_int < idx_range[1])] = True
            for tar in targets:
                input_data = self.expdata.get_data(tar)
                if type(input_data) != None:
                    input_data = np.moveaxis( input_data, mean_ax, -1)
                    output_data[tar] = np.mean(input_data,axis=-1, where=bool_filter)

            self.expdata.exp_vars.pop(mean_ax)
            new_exp_vars = self.expdata.exp_vars
            new_config = self.expdata.configs
            new_config[axis] = "Meaned"
            self.expdata = ExpData(new_exp_vars,output_data,new_config)

        return self.expdata
    
    def to_complex( self, real_part:str, image_part:str, output_name:str ):

        self.expdata.data[output_name] = self.expdata.data[real_part]+1j*self.expdata.data[image_part]
        return self.expdata
    
    def get_abs( self, targets:list[str], output_names:[str] ):

        for in_name, out_name in zip(targets, output_names):
            self.expdata.data[out_name] = np.abs(self.expdata.data[in_name])

        return self.expdata

    def get_angle( self, targets:list[str], output_names:[str] ):

        for in_name, out_name in zip(targets, output_names):
            self.expdata.data[out_name] = np.angle(self.expdata.data[in_name])
            
        return self.expdata