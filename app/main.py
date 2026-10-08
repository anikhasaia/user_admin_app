from fastapi import FastAPI

from .init_admin import create_admin

app = FastAPI()


@app.on_event("startup")
def startup():
    create_admin()


@app.get("/")
def root():
    return {
        "message": "Application is running"
    }