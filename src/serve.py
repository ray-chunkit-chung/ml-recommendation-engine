import os
import keras
import numpy as np

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from typing import List
from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.environ.get("MODEL_PATH")


class FeatureSet(BaseModel):
    UserIds: List[int]
    MovieIds: List[int]


def regressor(data: dict) -> dict:
    model = keras.models.load_model(MODEL_PATH)
    user_ids = data["UserIds"]
    movie_ids = data["MovieIds"]
    user_movie_combinations = [
        (user_id, movie_id) for user_id in user_ids for movie_id in movie_ids
    ]
    user_movie_combinations = np.array(user_movie_combinations)
    result = (
        model.predict([user_movie_combinations[:, 0], user_movie_combinations[:, 1]])
        .ravel()
        .tolist()
    )
    result = jsonable_encoder({"prediction": result})
    return JSONResponse(content=result)


ml_models = {}


@asynccontextmanager
async def ml_lifespan_manager(app: FastAPI):
    ml_models["regressor"] = regressor
    yield
    ml_models.clear()


app = FastAPI(lifespan=ml_lifespan_manager)


@app.post("/predict")
async def predict(feature_set: FeatureSet):
    return ml_models["regressor"](feature_set.dict())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
