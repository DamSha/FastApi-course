import secrets

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

app = FastAPI()
# Add Rate Limiter
# Max 3/sec : 1 token_expired + 1 get_token + 1 API call
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["3/second"],
)
# limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# Add Limiter Globally
# Send 429 status with details {"error":"Rate limit exceeded: 1 per 1 second"}
app.add_middleware(SlowAPIMiddleware)

# Encrypted Tokens from the database
token = secrets.token_urlsafe(32)
print("token:", token)
api_keys = [token, "GS7CBVwKjB5dGbqQ-iv-iTbvBHKwn5N58MF_cEp-W4o"]

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
async def root(request: Request, response: Response):
    return {"message": "Hello World"}


@app.get("/health_check")
# @limiter.exempt
async def health_check(request: Request, response: Response):
    # Do Health Check...
    return {"message": "Health Check OK !"}


@app.get("/posts/", dependencies=[Depends(api_key_auth)])
async def get_posts(request: Request, response: Response) -> dict:
    return {"message": "all posts"}


@app.post("/posts/")
async def save_post(request: Request, response: Response, new_post: Post):
    return {"message": f"Hello {new_post.model_dump_json()}"}


if __name__ == "__main__":
    uvicorn.run(app)
