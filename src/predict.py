import numpy as np
import pandas as pd
import keras

TRAIN_PATH = "../local/train.csv"
TEST_PATH = "../local/test.csv"
MODEL_PATH = "../local/model.h5"

# load data and model
train = pd.read_csv(TRAIN_PATH)
test = pd.read_csv(TEST_PATH)
model = keras.models.load_model(MODEL_PATH)

# print(train.query("user_id == 1242").shape[0])
# print(test.query("user_id == 1242").shape[0])

# Make predictions
user_ids = [1, 1242]  # Replace with user IDs you want to make recommendations for
movie_ids = list(
    range(1, len(train["movie_id"].unique()) + 1)
)  # Replace with movie IDs you want to recommend
user_movie_combinations = [
    (user_id, movie_id) for user_id in user_ids for movie_id in movie_ids
]
user_movie_combinations = np.array(user_movie_combinations)

predictions = model.predict(
    [user_movie_combinations[:, 0], user_movie_combinations[:, 1]]
)
recommendations = pd.DataFrame(
    {
        "user_id": user_movie_combinations[:, 0],
        "movie_id": user_movie_combinations[:, 1],
        "predicted_rating": predictions.ravel(),
    }
)
recommendations = recommendations.sort_values(by="predicted_rating", ascending=False)

# Top 10 recommendations for each user
print(recommendations.query("user_id == 1242").head(10))
print(recommendations.query("user_id == 1").head(10))
