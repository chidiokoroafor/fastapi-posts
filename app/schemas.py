
from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostRequest(PostBase):
    pass
    

        
class UserResponse(BaseModel):
    email: EmailStr
    id: int
    
    class Config:
        orm_mode = True
    
    
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    class Config:
        orm_mode = True

class PostWithVote(BaseModel):
    Post:PostResponse
    votes:int
           
           
           
class UserRequest(BaseModel):
    email: EmailStr
    password: str
    
 
     
class UserLogin(BaseModel):
    email: EmailStr
    password: str
     
class Token(BaseModel):
    access_token: str
    token_type: str
    
    class Config:
        orm_mode = True
     
class TokenData(BaseModel):
    id: str | None = None
    email: str | None = None
    
class Vote(BaseModel):
    post_id: int
    vote_dir:int = 0 | 1
    
    
    
    