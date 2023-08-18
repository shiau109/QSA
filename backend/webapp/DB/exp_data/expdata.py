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

class ExpData:
    '''
    The format of the data should follow the rule:
    2. setting a list about experiment.
    setting format is (name, numpy array)
    3. data record numerical value in numpy ndarray.
    '''
    def __init__( self, exp_vars:list, data:dict, configs:dict={} ):
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

    def __is_linked_var( self, exp_var:tuple )->bool:
        if isinstance(exp_var[0], list) and len(exp_var[0]) > 1 :
            return True
        else:
            return False
    
    def __check_exp_vars( self, exp_vars:list )->int:
        """
        If all the linked exp var have same length, return true and register self.__exp_vars, else return false
        """
        checked_exp_vars = []
        for ev in exp_vars:
            input_name = ev[0]
            input_vals = ev[1]
            # Check and rebuild input format
            # if not isinstance(input_name, list):
            #     input_name = list(input_name)

            if self.__is_linked_var(input_name):
                for i, n in enumerate(input_name):
                    ref_len = len(input_vals[0])
                    if len(input_vals[i]) != ref_len:
                        print(f"Waring!! Length of linked exp var {n} is not {ref_len} as {input_name[0]}")
                        return False
            
            checked_exp_vars.append((input_name, input_vals))
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
        find axis indexby the setting name.
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
            names = [setting_info[0]]
            for n in names:
                if n == name:
                    return i
        print(f"Setting name {name} can't be found")
        return None
    
    def resturcture( self, new_order:tuple ):
        """
        new order ( 2,0,1 ) make 2 axis to 0, 0 axis to 1, 1 axis to 2
        """
        data_dim = len(self.exp_vars)
        new_setting = []
        # Reset setting order
        for new_i in new_order:
            new_setting.append(self.exp_vars[new_i])
        self.__exp_vars = new_setting

        # Reshape data dimension
        for name, data in self.data.items():
            self.__data[name] = np.moveaxis( data, new_order, [*range(data_dim)] )
    def to_DataFrame( self )->DataFrame:
        data_shape = list(self.shape)
        flat_exp_vars = {}
        for axis, ev in enumerate(self.exp_vars):
            repeat_length = 1
            for i in data_shape[axis+1:]:
                repeat_length*=i
            axis_length = data_shape[axis]
            full_shape = data_shape[:axis]+[axis_length*repeat_length]
            if self.__is_linked_var(ev):
                names = ev[0]
                exp_vals = ev[1]
            else:
                names = [ev[0]]
                exp_vals = [ev[1]]
            for i, n in enumerate(names):
                v = exp_vals[i]
                repeat_part = np.full(tuple((repeat_length,axis_length)),v).flatten('F')
                stack_exp_vars = np.full(tuple(full_shape),repeat_part)
                # print("nD shape ", stack_exp_vars.shape)
                # print("flatten ",stack_exp_vars.flatten().shape)
                flat_exp_vars[n] = stack_exp_vars.flatten()
        new_df = DataFrame(flat_exp_vars)
        for col_name, nd_data in self.data.items():
            new_df[col_name] = nd_data.flatten()

        return new_df
    def get_subdata( self, address:list )->ExpData:
        """
        Get a copy of the part of this object 
        """
        data_dim = len(self.exp_vars)
        selected_axis = []
        remain_axis = []
        selected_address = []
        for axis, address_idx in enumerate(address):
            if address_idx == -1:
                remain_axis.append( axis )
            else:
                selected_axis.append( axis )

        selected_address = [ address[i] for i in selected_axis]
        new_structure = selected_axis+remain_axis
        sub_expData = copy.deepcopy(self)
        sub_expData.resturcture( new_structure )

        for axis, address in enumerate(selected_address):
            selected_exp_var = sub_expData.exp_vars.pop(0)
            name = selected_exp_var[0]
            val = selected_exp_var[1]
            
            if self.__is_linked_var(selected_exp_var):
                for i, n in enumerate(name):
                    sub_expData.configs[n] = val[i][address]
            else:
                sub_expData.configs[name] = val[address]


            for dname, data in sub_expData.data.items():
                print(dname, data.shape)
                sub_expData.__data[dname] = data[address]
        return sub_expData

    def get_data( self, name:str )->np.ndarray:
        data_names = self.data.keys()
        if name in data_names:
            return self.data[name]
        else:
            print("No data names in {name}")
            return None
        
if __name__ == '__main__':

    setting = [(["x","x1"],np.array([[0,1],[10,11]])),("y",np.array([4,5,6])),("z",np.array([-1,-2,-3,-3]))]
    rawdata = {
        "I":np.array([[[1,2,3,4],[5,6,7,8],[9,10,11,12]],[[21,22,23,24],[25,26,27,28],[29,30,31,32]]])
    }
    myData = ExpData(setting,rawdata)
    print( myData.to_DataFrame() )
    # print( myData.configs )
    # print( myData.get_structure_info())
    print( myData.shape)
    # myData.resturcture([2,1,0])
    # print( myData.configs )
    # print( myData.get_axis_idx("z"))
    # print( myData.get_axis_name(0))
    # print( myData.shape )
    # print( myData.dimension )
    newExpData = myData.get_subdata([1,-1,1])
    print( newExpData.configs )
    print( newExpData.exp_vars)
    # print( newExpData.get_axis_name(0))
    print( newExpData.shape )
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
