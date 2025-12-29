from fastapi import FastAPI , Response, status, HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# creating a list to hold our posts
my_post = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
           {"title": "title of post 2", "content": "content of post 2", "id": 2}]

# helper functions
def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i ,p in enumerate(my_post):
        if p['id'] == id:
            return i
        
# here we define our first route
@app.get("/")
def root():
    return {"message": "Hello World"}

# here we define a route to get posts


@app.get("/posts")
def get_posts():
    return {"data": my_post}

# here we define a route to create a post


@app.post("/createpost" ,status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_post.append(post_dict)
    return {"data": post_dict}  


# here we define a route to get a specific post by id

@app.get("/posts/{id}")
def get_post(id : int , response :Response):
    post = find_post(id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found") 
   #if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND 
        #return {"message": f"post with id: {id} was not found"} 
    post = find_post(id)
    print(post)
    return {"post_detail": post}


#here we will delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# here we will update a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {"data": post_dict}
