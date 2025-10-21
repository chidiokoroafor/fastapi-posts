from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import  engine
from app import models
from app.routers import post, user, auth, vote

app = FastAPI()

# models.Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"]
    )

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"Hello World"}












 