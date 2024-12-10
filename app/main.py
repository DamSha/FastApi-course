import json

import joblib
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
# from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.suggestor.suggestor import Suggestor

# https://www.youtube.com/watch?v=0sOvCWFmrtA
description = """
# Test FastAPI to do awesome stuff. 🚀
## Usage
- POST to **/path-to-test**
- with title/body
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

# origins = [
#     # "http://localhost",
#     "http://localhost:8000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


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


# model_non_supervise = joblib.load("./models/model_non_supervise.pkl")

#
# @app.get("/predict/non_supervise", tags=["predict"])
# async def predict_non_supervise(title_input, body_input):
#     """
#     Get predict non supervise
#     :return: {"message": [predictions]}
#     """
#     results_ns = suggestor.predict(title_input, body_input, False, .1)
#     predictions_ns = [[f"{p["tag"]}", round(p["proba"], 3)] for p in results_ns.to_dict(orient="records")]
#     return JSONResponse(content=jsonable_encoder(predictions_ns))
#     # {"tags - non supervisé": json.dumps(predictions_ns)}


@app.get("/predict", tags=["predict"])
async def predict_supervise(title_input, body_input):
    """
    Get predict supervise
    :return: {"message": [predictions]}
    """
    suggestor = Suggestor()
    results_s = suggestor.predict(title_input, body_input, True, .1)
    predictions_s = [[f"{p["tag"]}", round(p["proba"], 3)] for p in results_s.to_dict(orient="records")]
    return JSONResponse(content=jsonable_encoder(predictions_s))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", workers=1)
