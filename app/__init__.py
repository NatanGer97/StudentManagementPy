import uvicorn
from fastapi import FastAPI

from app.main.controller import student_controller
from app.main.database import engine, Base
from app.main.model import models

app = FastAPI()
app.include_router(student_controller.router)

models.Base.metadata.create_all(bind=engine);




@app.get("/")
async def root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)