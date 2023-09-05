




SET ENVNAME=FAST
call C:\ProgramData\Anaconda3\Scripts\activate.bat %ENVNAME%


:: qspp (editable installation, files are in PYQUM)
ECHO Installing ExpData
pip install -e ..\Dependency\expData

ECHO Installing DB_reader
pip install -e ..\Dependency\DB_reader

PAUSE