@echo off

ECHO WELCOME TO QAS


SET ENVNAME=FAST
call C:\ProgramData\Anaconda3\Scripts\activate.bat %ENVNAME%
@REM cd C:\Users\shiau\CAS\backend\webapp


uvicorn main:app --reload --host 0.0.0.0 --port 7999 




 