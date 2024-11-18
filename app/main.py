import importlib

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# https://www.youtube.com/watch?v=0sOvCWFmrtA
description = """
# Test FastAPI to do awesome stuff. 🚀
## Usage
- POST to **/path-to-test**
- with body/message
## Security
- Rate Limit : **3/second max**
## Author
- Damien Chauvet
"""

# importlib.metadata.version('app')
app = FastAPI(
    title="FastAPI-course",
    description=description,
    version="0.1.1",
)

app.mount('/report_pytest', StaticFiles(directory="reports/pytests/", html=True))
app.mount('/report_coverage', StaticFiles(directory="reports/test_coverage/", html=True))


class Post(BaseModel):
    title: str
    content: str


@app.get("/", tags=["Root"])
async def root():
    """
    Page d'accueil
    :return:
    """
    return {"message": "Hello World, updated by CI/CD"}


@app.get("/posts/", tags=["Posts"])
async def get_posts():
    """
    Get all posts
    :return:
    """
    return {"message": f"all posts"}


@app.post("/posts/", tags=["Posts"])
async def save_post(new_post: Post):
    """
    Save a post
    :param new_post:
    :return:
    """
    return {"message": f"Hello {new_post.model_dump_json()}"}
