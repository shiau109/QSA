from abc import ABCMeta, abstractmethod
from ast import literal_eval
from .series_str import SeriesStr
import numpy as np

# metaclass=ABCMeta
class PyqumShaper(metaclass=ABCMeta):

    @abstractmethod
    def import_header( self, header ):
        pass
        
    def check_header( self, header ):

        # Decode 
        header_str = header.decode('utf-8')

        # Basic structure
        header_dict = literal_eval( header_str )
        record_time = list(header_dict.keys())[0]
        raw_info = header_dict[record_time]
        check_list = ["c-order", "perimeter", "data-density"]
        for kname in check_list:
            if kname not in raw_info.keys():
                print(f"Warning!!! basic information {kname} not in header of pyqum data.")
                return False
        self.raw_info = raw_info
        return True
    @property
    def data_names( self )->list:
        dd = self.raw_info["data-density"]
        if isinstance( dd, list ):
            return None
        else:
            if dd == 2:
                return ["I","Q"]
            else:
                return None



    @abstractmethod
    def perimeter_praser( self, perimeter ):
        pass
    @abstractmethod
    def c_order_praser( self, c_order ):
        pass

class FResponseShape(PyqumShaper):
    axis_order = ["Flux-Bias", "S-Parameter", "IF-Bandwidth", "Power", "Frequency"]
    def __init__( self ):
        pass

    def import_header( self, header )->list:
        settings = []
        if self.check_header( header ):
            settings.extend(self.c_order_praser(self.raw_info["c-order"]))
        return settings  

    def perimeter_praser( self, perimeter ):
        pass
        # print(perimeter.keys())

    def c_order_praser( self, c_order ):
        settings = []
        for name in self.axis_order:
            if name in c_order.keys():
                setting_obj = SeriesStr( c_order[name] )
                settings.append( ( name, np.array(setting_obj.data) ) )

            else:
                print(f"{self.__class__} Warning!!! {name} not in c-order.")
        return settings 

class CWSweepShape(PyqumShaper):
    axis_order = ["Flux-Bias", "XY-Frequency", "XY-Power", "S-Parameter", "IF-Bandwidth", "Frequency", "Power"]
    def __init__( self ):
        pass

    def import_header( self, header ):
        settings = []
        if self.check_header( header ):
            settings.extend(self.c_order_praser(self.raw_info["c-order"]) )
        return settings 

    def perimeter_praser( self, perimeter ):
        pass
        # print(perimeter.keys())

    def c_order_praser( self, c_order ):
        settings = []

        for name in self.axis_order:
            if name in c_order.keys():
                setting_obj = SeriesStr( c_order[name] )
                settings.append( (name, np.array(setting_obj.data) ) )
                inner_reapeat = setting_obj.inner_repeat
                if inner_reapeat > 1:
                    settings.append( (f"{name}_inner_repeat", np.linspace(1,inner_reapeat,inner_reapeat)) )

            else:
                print(f"{self.__class__} Warning!!! {name} not in c-order.")
        return settings 

class SingleQubitShape(PyqumShaper):

    def __init__( self ):
        pass

    def import_header( self, header ):
        settings = []
        if self.check_header( header ):
            settings.extend(self.perimeter_praser(self.raw_info["perimeter"]) )
        return settings 

    def perimeter_praser( self, perimeter ):
        p_key = perimeter.keys()
        settings = []
                    
        if "R-JSON" in p_key:
            r_json = literal_eval( perimeter["R-JSON"] )
            for name, str_cmd in r_json.items():
                setting_obj = SeriesStr( str_cmd )
                settings.append( (name, np.array(setting_obj.data) ) )

        # Ratis for multiplex readout
        if "READOUTYPE" in p_key:
            if "IF_ALIGN_KHZ" in p_key and perimeter["READOUTYPE"]=="one-shot":
                IF_ALIGN_KHZ = np.array(perimeter["IF_ALIGN_KHZ"].split(" ")) # list -> ndarray
                settings.append( ("IF_ALIGN_KHZ", IF_ALIGN_KHZ) )


        # print(settings)
        if "READOUTYPE" in p_key:
            readout_mode = perimeter["READOUTYPE"]
            match readout_mode:
                case "continuous":
                    record_name = "RECORD_TIME_NS"
                    record_time = int(perimeter["RECORD_TIME_NS"])
                    time_res = int(perimeter["TIME_RESOLUTION_NS"])
                    record_length = int(record_time//time_res)
                    setting_val = np.linspace(0, record_time, record_length,endpoint=False)
                case "one-shot":
                    record_name = "RECORD-SUM"
                    shot_times = int(perimeter["RECORD-SUM"])
                    setting_val = np.linspace(0, shot_times, shot_times,endpoint=False)

                case _:
                    record_name = None

            settings.append((record_name, setting_val) )
        # print(settings)
        return settings
    
    def c_order_praser( self, c_order ):
        pass