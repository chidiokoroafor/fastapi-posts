from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from app.database import get_db, Base
from app.main import app
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .database import client, session

# Base.metadata.create_all(engine)

# Base = declarative_base()


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200
    
def test_create_user(client):
    res = client.post("/users", json={"email":"stan@mail.com", "password":"password"})
    assert res.status_code == 201
    assert res.json().get("email") == "stan@mail.com"
    
def test_login(client):
     res = client.post("/login", data={"username":"stan@mail.com", "password":"password"})
     
     assert res.status_code == 200