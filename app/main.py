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
	return {"status":"success"}