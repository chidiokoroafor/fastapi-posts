from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session = Depends(get_db), current_user:schemas.UserResponse = Depends(get_current_user)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id and models.Vote.user_id == current_user.id)
    vote_data = vote_query.first()
    
    if vote.vote_dir == 1:
        if vote_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="you cannot vote two times")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"success":"Your vote is added successfully"}
    else:
        if not vote_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No vote from the user")
        vote_query.delete()
        db.commit()
        return {"success":"Your vote is deleted successfully"}