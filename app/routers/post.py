from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)
# , response_model=list[schemas.PostWithVote]
@router.get("/", response_model=list[schemas.PostWithVote])
def get_posts(db: Session = Depends(get_db), current_user:schemas.UserResponse = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    # posts = db.query(models.Post).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    return results # [dict(row._mapping) for row in results]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post:schemas.PostRequest, db: Session = Depends(get_db), current_user:schemas.UserResponse = Depends(get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content,published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # conn.commit()
    # new_post = cursor.fetchone()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostWithVote)
def get_post(id:int,db: Session = Depends(get_db), current_user:schemas.UserResponse = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE Id = %s""", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not permited to view this post")
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    return results

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user:schemas.UserResponse = Depends(get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE Id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not permited to delete this post")
    
    db.delete(post)
    db.commit()
    return {"message":"post deleted successfully"}

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, post:schemas.PostRequest, db: Session = Depends(get_db), current_user:schemas.UserResponse = Depends(get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", ( post.title, post.content, post.published, id))
    # conn.commit()
    # post = cursor.fetchone()
    # conn.commit()
    db_query = db.query(models.Post).filter(models.Post.id == id)
    post_data = db_query.first()
    if post_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post_data.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not permited to update")
    
    db_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return db_query.first()