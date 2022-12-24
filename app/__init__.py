import uvicorn
from fastapi import FastAPI
from fastapi import BackgroundTasks

from app.main.controller import student_controller, grades_controller,email_controller, auth_controller
from app.main.database import engine, Base
from app.main.model import models
from app.main.services import email_service

app = FastAPI()
app.include_router(student_controller.router)
app.include_router(grades_controller.router)
app.include_router(email_controller.router)
app.include_router(auth_controller.router)

models.Base.metadata.create_all(bind=engine)

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)