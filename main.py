from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from access.cors_site import origins

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)