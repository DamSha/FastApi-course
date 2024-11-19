from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

origins = [
    # "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    return {"message": "all posts"}


@app.post("/posts/", tags=["Posts"])
async def save_post(new_post: Post):
    """
    Save a post
    :param new_post:
    :return:
    """
    return {"message": f"Hello {new_post.model_dump_json()}"}
