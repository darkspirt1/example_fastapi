from fastapi import FastAPI
from fastapi.params import Body
app = FastAPI()

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
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"title": payload['title'], "content": payload['content']}
