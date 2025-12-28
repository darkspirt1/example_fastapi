from fastapi import FastAPI
from fastapi.params import Body
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"posts": ["Post 1", "Post 2", "Post 3"]}


@app.post("/createpost")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"title": payload['title'], "content": payload['content']}
