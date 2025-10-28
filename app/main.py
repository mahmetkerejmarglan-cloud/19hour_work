
from fastapi import FastAPI,  status, HTTPException,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import model,schemas,utils
from .database import  engine
from .routers import user,post,auth,vote
from .config import settings   
from fastapi.middleware.cors import CORSMiddleware


model.Base.metadata.create_all(bind=engine)

print(settings.database_username)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "Hello wirl"}








#registration and login for userrrrrsssss

