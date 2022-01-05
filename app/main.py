from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app=FastAPI()

#pydantic model
class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    #rating:Optional[int]=None

#connetction statement for postgres database
while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',port='5432',user='postgres',password='passkey',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Connected")
        break
    except Exception as e:
        print("Connection to database failed")
        print("Error",e)
        time.sleep(2)


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
    cursor.execute("""SELECT * FROM posts""") #sql statements
    posts=cursor.fetchall()
    return {"data":posts}

    #return {"data":my_posts}
    #return {"data":"This is your post"}

#router for create posts
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))#sanitizing data while inserting it
    new_post=cursor.fetchone()
    conn.commit()#stage changing to database it self
    return {"data":new_post}

    #print(post)
    #print(post.dict())
    #post_dict=post.dict()
    #post_dict['id']=randrange(0,1000000)
    #my_posts.append(post_dict)
    #return {"data":post_dict}
    



#router for posts with specific id
@app.get("/posts/{id}") #id refrenced as a path parameter
def get_post(id:int,response:Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    return{"data":post}


    #post=find_post(id)
    #if not post:
     #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    #return {"post_details":post}
        #unused code
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {'message':f"post with id:{id} not found"}
    #return{"Post Details":f"Here is the ID of the post+'{id}'"}
    


#delete posts 
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
    deleted_posts=cursor.fetchone()
    conn.commit()
    #index=find_index_post(id)
    if deleted_posts==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} does not exist")
    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    #return {'Message':'post was successfully deleted'}

#update a posts
@app.put("/posts/{id}")
def update_posts(id:int,post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    post_dict=cursor.fetchone()
    conn.commit()

    #index=find_index_post(id)
    if post_dict==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} does not exist")
    #post_dict=post.dict()
    #post_dict['id']=id 
    #my_posts[index]=post_dict   
    return {"data":post_dict}
