import os
import keras
import numpy as np
from operator import itemgetter

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
    # Load model and predict
    model = keras.models.load_model(MODEL_PATH)
    user_ids = data["UserIds"]
    movie_ids = data["MovieIds"]
    user_movie_combinations = [
        (user_id, movie_id) for user_id in user_ids for movie_id in movie_ids
    ]
    combination_array = np.array(user_movie_combinations)
    scores = (
        model.predict([combination_array[:, 0], combination_array[:, 1]])
        .ravel()
        .tolist()
    )

    # Sort result by highest score. Return top 12
    result = [
        (i[0], i[1], scores[idx]) for idx, i in enumerate(user_movie_combinations)
    ]
    result = sorted(result, key=itemgetter(2), reverse=True)[:12]

    # Format result
    result = [
        {
                "userId": user_id,
                "id": movie_id,
                "score": score, 
        } for user_id, movie_id, score  in result
    ]
    result = jsonable_encoder({'predictions': result})

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
