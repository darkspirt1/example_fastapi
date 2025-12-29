from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating : Optional[int] = None
# here we define our first route


@app.get("/")
def root():
    return {"message": "Hello World"}

# here we define a route to get posts


@app.get("/posts")
def get_posts():
    return {"posts": ["Post 1", "Post 2", "Post 3"]}

# here we define a route to create a post


@app.post("/createpost")
def create_post(post: Post):
    print(post)
    print(post.dict())
    return {"data": post}
