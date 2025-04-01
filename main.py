from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, Optional
#from typing import Optional
import models
from database import engine, Sessionlocal
from sqlalchemy.orm import Session
# metadata
import requests
from bs4 import BeautifulSoup

app = FastAPI()
# models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind = engine)

class PostBase(BaseModel):
    title: str
    content: str
    user_Id: int

class UserBase(BaseModel):
    #id: int
    username: str

class UserBase(BaseModel):
    #id: int
    username: str    

class Metadata(BaseModel):
    title: Optional[str] 
    description: Optional[str] 
    author: Optional[str]  

def get_db():
    db = Sessionlocal()
    try: 
        yield db

    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/posts/{post_Id}", status_code= status.HTTP_200_OK)
async def read_post(post_Id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_Id).first()
    if post is None:
        HTTPException(status_code=404, detail='Post was not found')
    return post


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()

@app.delete("/posts/{post_Id}", status_code= status.HTTP_200_OK)
async def delete_post(post_Id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Post was not found')
    db.delete(db_post)
    db.commit()


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()


@app.get("/users/{user_Id}", status_code= status.HTTP_201_CREATED)
async def read_user(user_Id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_Id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@app.delete("/users/{user_Id}", status_code= status.HTTP_200_OK)
async def delete_post(user_Id: int, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_Id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    db.delete(db_user)
    db.commit()

    ####### Links #####

# @app.post("/links/", status_code=status.HTTP_201_CREATED)
# async def create_link(user: LinkBase, db: db_dependency):
#     db_user = models.User(**user.dict())
#     db.add(db_user)
#     db.commit()    

# @app.get("/links/{link_Id}", status_code= status.HTTP_200_OK)
# async def read_link(link_Id: int, db: db_dependency):
#     link = db.query(models.Link).filter(models.Link.id == link_Id).first()
#     if link is None:
#         HTTPException(status_code=404, detail='Link was not found')
#     return link    

 ####### metadata #####



@app.get("/metadata", response_model=Metadata)
async def get_metadata(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, "html.parser")

        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else None

        description_tag = soup.find("meta", attrs={"name": "description"})
        description = description_tag.get("content").strip() if description_tag else None

        author_tag = soup.find("meta", attrs={"name": "author"})
        author = author_tag.get("content").strip() if author_tag else None

        metadata = Metadata(title=title, description=description, author=author)
        return metadata
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {e}")
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
