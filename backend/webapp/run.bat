@echo off


:: This batch file runs pyqum v0.1
ECHO WELCOME TO QAS


SET ENVNAME=FAST
call C:\ProgramData\Anaconda3\Scripts\activate.bat %ENVNAME%
cd C:\Users\shiau\CAS\backend\webapp
uvicorn main:app --reload




