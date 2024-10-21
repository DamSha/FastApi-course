from fastapi import FastAPI
from pydantic import BaseModel

# https://www.youtube.com/watch?v=0sOvCWFmrtA
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
async def root():
    """
    Page d'accueil
    :return:
    """
    return {"message": "Hello World, updated by CI/CD"}


@app.get("/posts/")
async def get_posts():
    """
    Get all posts
    :return:
    """
    return {"message": f"all posts"}


@app.post("/posts/")
async def save_post(new_post: Post):
    """
    Save a post
    :param new_post:
    :return:
    """
    return {"message": f"Hello {new_post.model_dump_json()}"}
