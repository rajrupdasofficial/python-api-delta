from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models 

from database import engine,get_db  #sessionLocal

#main code for bind and create sqlalchemy ORM quaries
models.Base.metadata.create_all(bind=engine)

#initializing fastapi
app=FastAPI()



@app.get("/")
def test_posts(db:Session=Depends(get_db)):
	posts=db.query(models.Post).all()
	return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post,db:Session=Depends(get_db)):
	newpost=models.Post(title=post.title,content=post.content,published=post.published)
	db.add(newpost)
	db.commit()
	db.refresh(newpost)
	return {"data":newpost}
