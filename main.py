# main.py

from fastapi import FastAPI
from core.config import Settings
from db.session import engine
from db.base_class import Base

def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=Settings.PROJECT_NAME,version=Settings.PROJECT_VERSION)
    create_tables()
    return app


app = start_application()


@app.get("/")
def hello_api():
    return {"msg":"Hello FastAPI🚀"}

