
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dependencies import get_query_token, get_token_header
from internal import admin
# from routers import items, users
from searching import searching
from job import job
from sample import sample
from analysis import resonator, single_shot, T1_analysis

# app = FastAPI(dependencies=[Depends(get_query_token)])

app = FastAPI()


# app.include_router(users.router)
# app.include_router(items.router)
app.include_router(job.router)
app.include_router(resonator.router)
app.include_router(single_shot.router)

app.include_router(searching.router)
app.include_router(sample.router)

app.include_router(T1_analysis.router)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

origins = [
    # "http://localhost",
    "http://localhost:4200",
    "http://192.168.1.150:4200",
    "http://192.168.1.135:4200",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}




