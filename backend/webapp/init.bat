




SET ENVNAME=FAST
call C:\ProgramData\Anaconda3\Scripts\activate.bat %ENVNAME%


conda env create -f environment.yml

:: qspp (editable installation, files are in PYQUM)
ECHO Installing ExpData
pip install -e ..\Dependency\expData

ECHO Installing DB_reader
pip install -e ..\Dependency\DB_reader

ECHO Installing resonator_tools
pip install -e ..\Dependency\resonator_tools

ECHO Installing single_shot
pip install -e ..\Dependency\single_shot

PAUSE