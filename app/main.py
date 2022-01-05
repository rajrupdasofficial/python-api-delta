from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app=FastAPI()

#pydantic model
class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    #rating:Optional[int]=None

try:
    conn=psycopg2.connect(host='localhost',database='fastapi',port='5432',user='postgres',password='passkey',cursor_factory=RealDictCursor)
    cursor=conn.cursor
    print("Connected")
except Exception as e:
    print("Connection to database failed")
    print("Error",e)


#simple structures 
#def create_posts(payload: dict = Body(...)):
 #   print(payload)
   # return {"Message":"Post Successfully created"}
  #  return {"new_posts":f"title{payload['title']} content: {payload['content']}"}


#global variable decleared array to hold posts in a list in memory
my_posts=[{"title":"title post 1", "content":"content 1", "id":1},{"title":"favorite foods","content":"I like Pizza", "id":2}]

def find_post(id):
    for p in my_posts:
        if p ["id"]==id:
            return p

def find_index_post(id):
    for i,p  in enumerate(my_posts):
        if p['id']==id:
            return i

#redirection paths 

#simple message on main page
@app.get("/")
async def root():
    return {"message":"Hell YEAH!- API Running"}


#router for getting all posts
@app.get("/posts")
def get_posts():
    return {"data":my_posts}
    #return {"data":"This is your post"}

#router for create posts
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    print(post)
    print(post.dict())
    post_dict=post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

#router for posts with specific id
@app.get("/posts/{id}") #id refrenced as a path parameter
def get_post(id:int,response:Response):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    return {"post_details":post}
        #unused code
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {'message':f"post with id:{id} not found"}
    #return{"Post Details":f"Here is the ID of the post+'{id}'"}
    


#delete posts 
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index=find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    #return {'Message':'post was successfully deleted'}

#update a posts
@app.put("/posts/{id}")
def update_posts(id:int,post:Post):
    index=find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} does not exist")
    post_dict=post.dict()
    post_dict['id']=id 
    my_posts[index]=post_dict   

    return {"data":post_dict}
