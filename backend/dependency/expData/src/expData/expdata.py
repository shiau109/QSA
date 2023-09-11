from __future__ import annotations        

from pathlib import Path

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os import stat, SEEK_END
import ast
from json import loads
import numpy as np

from time import time
from abc import ABCMeta, abstractmethod
import copy
from pandas import DataFrame

from typing import TypedDict

class DataAddress( TypedDict ):
    var_name: str
    position: list[int]
    axis: int



class ExpData:
    '''
    The format of the data should follow the rule:
    2. exp_vars is setting a list about experiment.
        setting format is (name, numpy array)
    3. data record numerical value in numpy ndarray.
        {  "name": numpy array,  }
    '''
    def __init__( self, exp_vars:list[dict[str,np.ndarray]], data:dict, configs:dict={} ):
        self.__configs = configs
        self.__data = data
        if self.__check_exp_vars(exp_vars):
            self.__exp_vars = exp_vars

        if not self.__check_shape():
            self.__exp_vars = None
            self.__data = None
            print("Construnction of ExpData failed")
    @property    
    def data( self )->dict:
        """
        All data 
        """
        return self.__data

    @property    
    def exp_vars( self )->list:
        """
        All explanatory variable 
        """
        return self.__exp_vars
    @property    
    def configs( self )->dict:
        """
        All configuration settings 
        """
        return self.__configs
    @property
    def dimension( self )->int:
        shape = self.shape
        if shape is None:
            return None
        else:
            return len(shape)
    @property
    def shape( self ):
        if self.__check_shape():
            return self.__setting_shape()
        else:
            return None
    
    def get_structure_info( self )->list:
        structure_info = []
        for exp_v in self.exp_vars:
            structure_info.append((exp_v[0],len(exp_v[1])))
        return structure_info


    def __setting_shape( self ):
        setting_shape = []
        for linked_setting in self.exp_vars:            
            setting_shape.append( len(linked_setting[1]) )

        return tuple(setting_shape) 

    def __data_shape( self ):
        data_shape = None
        for name, data in self.data.items():
            if data_shape is None:
                data_shape = data.shape
            elif data_shape != data.shape:
                print(f"Shape of data {name} {data.shape} is not capatible with other {data_shape}")
                return None
        return data_shape

    def __is_linked_var( self, exp_var_idx:int )->bool:
        exp_var = self.exp_vars[exp_var_idx]
        if isinstance(exp_var[0], list) and len(exp_var[0]) > 1 :
            return True
        else:
            return False
    
    def __check_exp_vars( self, exp_vars:list )->int:
        """
        If all the linked exp var have same length, return true and register self.__exp_vars, else return false
        """
        self.__exp_vars = []
        for i, ev in enumerate(exp_vars):
            input_name = ev[0]
            input_vals = ev[1]
            # Check and rebuild input format
            # if not isinstance(input_name, list):
            #     input_name = list(input_name)
            self.__exp_vars.append(ev)
            if self.__is_linked_var(i):
                for i, n in enumerate(input_name):
                    ref_len = len(input_vals[0])
                    if len(input_vals[i]) != ref_len:
                        print(f"Waring!! Length of linked exp var {n} is not {ref_len} as {input_name[0]}")
                        return False
            
        return True

    
    
    def __check_shape( self ):
        """
        If shape of data is the same as setting, return true
        """
        s_shape = self.__setting_shape()
        d_shape = self.__data_shape()
        if s_shape == d_shape:
            return True
        else:
            print(f"Shape of data {d_shape} is not capatible with setting {s_shape}")
            return False

    def get_axis_name( self, axis_idx = None )->int:
        """
        find axis index by the setting name.
        """
        setting_dim = len(self.exp_vars)
        if axis_idx is None:
            axis_names = []
            for setting_info in self.exp_vars:
                axis_names.append(setting_info[0])
            return axis_names
        elif axis_idx >= setting_dim:
            print(f"Index {axis_idx} is larger than setting dimension")
            return None
        else:
            setting_info = self.exp_vars[axis_idx]
            axis_name = setting_info[0]
            return axis_name


    def get_axis_idx( self, name )->int|None:
        """
        find axis index by the setting name.
        """
        for i, setting_info in enumerate(self.exp_vars):
            names = setting_info[0]
            if not self.__is_linked_var(i):
                names = [setting_info[0]]
            for n in names:
                if n == name:
                    return i
        print(f"Setting name {name} can't be found")
        return None
    
    def resturcture( self, selected_axes:list[str], new_axes:list[int] ):
        """
        selected_axes : name of var
        new_axes : idx for new axis
        """
        # Reset setting order
        for selected_name, new_axis in zip(selected_axes, new_axes):
            if new_axis<0:
                new_axis = self.dimension+new_axis
            original_axis = self.get_axis_idx(selected_name)
            selected_var = self.exp_vars.pop(original_axis)
            self.exp_vars.insert( new_axis, selected_var)
            # print("temp",selected_name, original_axis, "to", new_axis, self.exp_vars)
        # Reshape data dimension
            for name, data in self.data.items():
                self.__data[name] = np.moveaxis( data, original_axis, new_axis )

    def to_DataFrame( self )->DataFrame:
        data_shape = list(self.shape)
        flat_exp_vars = {}
        for axis, ev in enumerate(self.exp_vars):
            repeat_length = 1
            for i in data_shape[axis+1:]:
                repeat_length*=i
            axis_length = data_shape[axis]
            full_shape = data_shape[:axis]+[axis_length*repeat_length]
            if self.__is_linked_var(axis):
                names = ev[0]
                exp_vals = ev[1]
            else:
                names = [ev[0]]
                exp_vals = [ev[1]]
            for i, n in enumerate(names):
                v = exp_vals[i]
                repeat_part = np.full(tuple((repeat_length,axis_length)),v).flatten('F')
                stack_exp_vars = np.full(tuple(full_shape),repeat_part)
                flat_exp_vars[n] = stack_exp_vars.flatten()
        new_df = DataFrame(flat_exp_vars)
        for col_name, nd_data in self.data.items():
            new_df[col_name] = nd_data.flatten()

        return new_df
    def get_subdata( self, address:list[DataAddress] )->ExpData:
        """
        Get a copy of the part of this object 
        """
        sub_expData = copy.deepcopy(self)
        for a_info in address:
            print(a_info)
            selected_pos = np.array(a_info["position"],dtype = int)
            name = a_info["var_name"]
            new_axis =  a_info["axis"]
            if selected_pos[0] == -1:
                """
                Select all
                """
                sub_expData.resturcture([name],[new_axis])
            elif len(selected_pos) == 1:
                """
                Only one is selected in the axis, dimension will -1
                """
                sub_expData.resturcture([name],[0])
                selected_pos = selected_pos[0]
                # Slice data
                for dname, data in sub_expData.data.items():
                    sub_expData.__data[dname] = data[selected_pos]
                # Modify exp_var   
                islinked =  sub_expData.__is_linked_var(0)
                sub_expData.resturcture([name],[0])
                selected_var = sub_expData.exp_vars.pop(0)
                if islinked:
                    for i, var in enumerate(selected_var):
                        
                        sub_expData.configs[var[0][i]] = var[1][i][selected_pos]
                else:
                    sub_expData.configs[selected_var[0]] = selected_var[1][selected_pos]

            else:
                """
                Multi-value is selected in the axis, dimension will not change
                """
                sub_expData.resturcture([name],[0])
                for dname, data in sub_expData.data.items():
                    # Slice data
                    sub_expData.__data[dname] = data[selected_pos]
                    selected_var = sub_expData.__exp_vars[0]
                    if not sub_expData.__is_linked_var(0):
                        sub_expData.__exp_vars[0] = (selected_var[0],selected_var[1][selected_pos])
                    else:
                        new_var = []
                        for val in selected_var[1]:
                            new_var.append(val[selected_pos])
                        sub_expData.__exp_vars[0][1] = new_var 

                sub_expData.resturcture([name],[new_axis])

    
        return sub_expData

    def get_data( self, name:str )->np.ndarray:
        """
        Get data by the name
        """
        data_names = self.data.keys()
        if name in data_names:
            return self.data[name]
        else:
            print("No data names in {name}")
            return None


    def get_var_vals( self, name:str )->np.ndarray:
        """
        Get data by the name
        """
        var_idx = self.get_axis_idx(name)
        if var_idx != None:
            if self.__is_linked_var(var_idx):
                linked_var = self.exp_vars[var_idx]
                link_idx = mylist.index(element)
                return linked_var[1][link_idx]
            else:
                var = self.exp_vars[var_idx]
                return var[1]
    # def to_npz( output ):



if __name__ == '__main__':

    setting = [(["x","x1"],np.array([[0,1],[10,11]])),("y",np.array([4,5,6])),("z",np.array([-1,-2,-3,-3]))]
    rawdata = {
        "I":np.empty((2,3,4))
    }
    myData = ExpData(setting,rawdata)
    # print( myData.to_DataFrame() )
    # print( myData.configs )
    print( myData.get_structure_info())
    print( myData.shape)
    # myData.resturcture(["y","x"],[0,1])
    # print("After resturcture")
    # print( myData.get_structure_info())
    # print( myData.shape)
    testTypedDict: DataAddress = {
            "var_name":"x",
            "position":[1],
            "axis":1,
        }
    print(DataAddress)
    subdata_address = [
        # {
        #     "var_name":"x",
        #     "position":[-1],
        #     "axis":-1,
        # },
        {
            "var_name":"y",
            "position":[-1],
            "axis":-1,
        },
                {
            "var_name":"z",
            "position":[-1],
            "axis":-1,
        }
    ]
    subdata = myData.get_subdata(subdata_address)
    print("Sub data")
    print( subdata.get_structure_info())
    print( subdata.shape)
    print("Origin data")
    print( myData.get_structure_info())
    print( myData.shape)
    # print( newExpData.get_axis_name(0))
    # print( newExpData.dimension )
    # new_data = np.moveaxis( data, [range(3)], list((1,0,2)) )
    # print( new_data )
    # print(setting)
    # colx = ["x",1,2]
    # coly = ["y",3,4]
    # test2 = np.array([colx,coly])
    # print(test2[:,0])
    # test1 = np.stack((colx,coly),axis=-1)
    # print(test1[0])
