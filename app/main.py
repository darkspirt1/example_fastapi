from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
#importing models and schemas
from .import models
from .database import engine, get_db
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres',
                                user='postgres', password='8928', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(5)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# creating a list to hold our posts
my_post = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
           {"title": "title of post 2", "content": "content of post 2", "id": 2}]

# helper functions


def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i

# here we define our first route


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"message": "Hello World sqlalchemy"}

# here we retrieve all posts from database

@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}
    

# here we define a route to create a post and add into database 


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """
                   ,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# here we define a route to get a specific post by id from database

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
   # if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}

    print(post)
    return {"post_detail": post}


# here we will delete a post from database
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# here we will update a post in database


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post ==  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    return {"data": updated_post}
