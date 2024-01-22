from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from .. import models, schema, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users"
)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schema.UserOut)
def create_users(user: schema.UserCreate,db: Session = Depends(get_db)):
    # post = models.Post(title = post.title,content= post.content, published= post.published)
    #Hashing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", status_code= status.HTTP_202_ACCEPTED, response_model= schema.UserOut)
def get_posts(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)

    if user.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    user.delete(synchronize_session=False)
    db.commit()