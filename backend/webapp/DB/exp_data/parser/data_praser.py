from abc import ABCMeta, abstractmethod
from os import stat, SEEK_END
from ..expdata import ExpData
from ast import literal_eval
from .pyqum.pyqum_shaper import PyqumShaper
import numpy as np
from os.path import splitext
from time import time
from colorama import Fore, Back

class ExpDataParser( metaclass=ABCMeta ):
    def __init__():
        pass
    @abstractmethod
    def import_data()->ExpData:
        pass  



class PyqumPraser( ExpDataParser ):

    def __init__( self ):
        pass

    def import_data( self, path )->ExpData:
        tStart = time()

        self.__path = path
        self.__check_data_address()

        self.__shaper_type()
        self.__shape_info = self.__shaper.import_header(self.__header)
        myExpData = self.__rebuild_data()
        print(Back.GREEN + Fore.WHITE + "DATA loaded in %ss" %(time()-tStart))

        return myExpData
    @property
    def data_address( self )->int:
        """
        The address that start to record data
        """
        return self.__data_address

    @property
    def file_size( self )->int:
        """
        The address that start to record data
        """
        return self.__file_size
    
    def __shaper_type( self )->PyqumShaper:
        from .pyqum.pyqum_shaper import FResponseShape, CWSweepShape, SingleQubitShape
        type_list = [ "Single_Qubit", "F_Response", "CW_Sweep" ]
        f_name = splitext(self.__path)[0]
        for t in type_list:
            if f_name.find(t) != -1:
                pyqum_type = t
        match pyqum_type: 
            case "Single_Qubit":
                self.__shaper = SingleQubitShape()
            case "CW_Sweep":
                self.__shaper = CWSweepShape()
            case "F_Response":
                self.__shaper = FResponseShape()
            case _:
                self.__shaper = SingleQubitShape()
    
    
    

    def __check_data_address( self ):
        '''
        Check the format is pyqum file
        '''
        file_path = self.__path
        file_size = stat(file_path).st_size
        self.__file_size = file_size
        with open(file_path, 'rb') as datapie:
            i = 0
            # Find data location
            while i < file_size:
                datapie.seek(i)
                bite = datapie.read(7)
                if bite == b'\x02' + bytes("ACTS", 'utf-8') + b'\x03\x04': # ACTS
                    end_of_header = i
                    break
                else: i += 1
            # Seperate header and data
            self.__data_address = end_of_header+7
            # Get header
            datapie.seek(0)
            self.__header = datapie.read( end_of_header )

    def __load_data(self):
        '''Loading the Data
            Return a 1D array
        '''
        data_size = self.__file_size -self.data_address
        # try:
        with open(self.__path, 'rb') as datapie:
            datapie.seek(self.data_address)
            
            pie = datapie.read(data_size)
            # self.selectedata = array(struct.unpack('>' + 'd'*((self.writtensize)//8), pie))
            data = np.ndarray(shape=(data_size//8,), dtype=">d", buffer=pie) # speed up with numpy ndarray, with the ability to do indexing in it.
        # except:
        #     # raise
        #     print(f"Failed to load data from {self.__path}")
        
        return data     


    def __rebuild_data( self ):
        """
        
        """
        # Check data size
        data = self.__load_data()
        data_density = len(self.__shaper.data_names)
        len_data = int(data.shape[-1]//data_density)
        # Check if the length from header and data is the same
        len_header = 1
        reshape_setting = []
        fixed_setting = {}
        changed_setting = []
        for name, vals in self.__shape_info:
            setting_len = vals.shape[-1]
            if setting_len > 1:
                reshape_setting.append(setting_len)
                len_header *= setting_len
                changed_setting.append( ( name, vals ) )
            else:
                fixed_setting[name] = vals[0]
        if len_data != len_header:
            print( f"Warning!!! Length from recored data {len_data} and header {len_header} are not the same." )
        reshape_setting.append(data_density)
        data = data.reshape( tuple(reshape_setting) )
        data = np.moveaxis( data, -1, 0)
        new_data = {}
        for i, d_name in enumerate(self.__shaper.data_names):
            new_data[d_name] = data[i]
            # print(d_name, data[i].shape)
        return ExpData( changed_setting, new_data, fixed_setting )