

from DB_reader.SQLite_parser import read_sql_lab

# TEST_DB_PATH = r"C:\Users\ASQUM\HODOR\CONFIG\pyqum.sqlite"
# TEST_DATA_PATH = r"C:/Users/ASQUM/HODOR/CONFIG/USRLOG"
TEST_DB_PATH = r"..\tests\pyqum.sqlite"
TEST_DATA_PATH = r"..\tests"
from expData.parser.data_praser import ExpDataParser, PyqumPraser
from expData.data_process import PrecessCMD, DataProcesser


def get_db_info( )->read_sql_lab:
    mySQL = read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)
    return mySQL

def get_job_header( job_ID ):
    mySQL = get_db_info()
    job_header = mySQL.get_job(job_ID)
    return job_header


def get_job_expdata( job_ID ):

    mySQL = get_db_info()
    job_data_path = mySQL.jobid_search_pyqum(job_ID)
    parser = PyqumPraser()
    job_data = parser.import_data(job_data_path)
    return job_data