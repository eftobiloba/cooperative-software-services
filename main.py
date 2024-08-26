from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from access.cors_site import origins
from routes.form import form_router
from routes.admin import admin_router
from routes.dev import dev_router
from routes.action import action_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(form_router, prefix="/forms")
app.include_router(admin_router, prefix="/admin")
app.include_router(dev_router, prefix="/dev")
app.include_router(action_router, prefix='/action')