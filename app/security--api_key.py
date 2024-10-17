import secrets

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from starlette import status

# https://www.youtube.com/watch?v=0sOvCWFmrtA
app = FastAPI()

# Encrypted Tokens from the database
token = secrets.token_urlsafe(32)
print("token:", token)
api_keys = [token, 'GS7CBVwKjB5dGbqQ-iv-iTbvBHKwn5N58MF_cEp-W4o']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def api_key_auth(_token: str = Depends(oauth2_scheme)):
    if _token not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API KEY refused.",
        )


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts/", dependencies=[Depends(api_key_auth)])
async def get_posts() -> dict:
    return {"message": f"all posts"}


@app.post("/posts/")
async def save_post(new_post: Post):
    return {"message": f"Hello {new_post.model_dump_json()}"}


if __name__ == "__main__":
    uvicorn.run(app)
