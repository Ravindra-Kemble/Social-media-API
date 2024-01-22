from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from .. import models, schema, oauth2
from typing import Optional, List
from sqlalchemy import func
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


#--------| CREATING A NEW POST |---------
@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate,db: Session = Depends(get_db),current_user: int =  Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return post

# -------| RETURNING ALL THE POST |-------
@router.get("/",response_model= List[schema.PostOut])
def posts(db: Session = Depends(get_db),limit: int = 10, search: Optional[str] = "", skip: int = 0 ):
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    
    # 1.query columns to get | 2.left outer join | 3. group by postid | 4. filter query | 5. limit query
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search))\
        .limit(limit).offset(skip).all()    
    
    return results
    # return posts

#--------| RETURNING POST BY ID |---------
@router.get("/{id}",response_model= schema.PostOut)
def get_posts(id: int, db: Session = Depends(get_db),current_user: int =  Depends(oauth2.get_current_user)):
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")

    return post
    
#---------| DELETING POST BY ID |----------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    
#----------| UPDATING POST BY ID |----------
@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def Update_post(id: int,updated_post: schema.PostBase, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()
