

from DB_reader.SQLite_parser import read_sql_lab

# TEST_DB_PATH = r"C:\Users\ASQUM\HODOR\CONFIG\pyqum.sqlite"
# TEST_DATA_PATH = r"C:/Users/ASQUM/HODOR/CONFIG/USRLOG"
TEST_DB_PATH = r"..\tests\pyqum.sqlite"
TEST_DATA_PATH = r"..\tests"

def get_dataInfo( ):
    return read_sql_lab(TEST_DB_PATH,TEST_DATA_PATH)