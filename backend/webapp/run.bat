@echo off

ECHO WELCOME TO QAS


SET ENVNAME=FAST
call C:\ProgramData\Anaconda3\Scripts\activate.bat %ENVNAME%
cd C:\Users\shiau\CAS\backend\webapp
uvicorn main:app --reload --port 7999 




 