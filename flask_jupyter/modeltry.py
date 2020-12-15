import pandas as pd
import numpy as np
from zipfile import ZipFile
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
import matplotlib.pyplot as plt

"""
## First, load the data and apply preprocessing
"""

# Download the actual data from http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
# Use the ratings.csv file
def raaah():

    movielens_data_file_url = ("http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
)
    movielens_zipped_file = keras.utils.get_file("ml-latest-small.zip", movielens_data_file_url, extract=False
)
    keras_datasets_path = Path(movielens_zipped_file).parents[0]
    movielens_dir = keras_datasets_path / "ml-latest-small"

# Only extract the data the first time the script is run.
    if not movielens_dir.exists():
        with ZipFile(movielens_zipped_file, "r") as zip:
        # Extract files
            print("Extracting all the files now...")
            zip.extractall(path=keras_datasets_path)
            print("Done!")

    ratings_file = movielens_dir / "ratings.csv"
    df = pd.read_csv(ratings_file)
    return df


def prepare_embedding(df):
    user_ids = df["userId"].unique().tolist()
    user2user_encoded = {x: i for i, x in enumerate(user_ids)}
    userencoded2user = {i: x for i, x in enumerate(user_ids)}
    movie_ids = df["movieId"].unique().tolist()
    movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
    movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}
    df["user"] = df["userId"].map(user2user_encoded)
    df["movie"] = df["movieId"].map(movie2movie_encoded)

    num_users = len(user2user_encoded)
    num_movies = len(movie_encoded2movie)
    df["rating"] = df["rating"].values.astype(np.float32)

# min and max ratings will be used to normalize the ratings later
    min_rating = min(df["rating"])
    max_rating = max(df["rating"])

    print(
    "Number of users: {}, Number of Movies: {}, Min rating: {}, Max rating: {}".format(
        num_users, num_movies, min_rating, max_rating)
    )
    #return num_users, num_movies, min_rating, max_rating
    #return pd.Series([e, f, g])
    #return np.array((e, f, g))
    #return pd.DataFrame((df["user"], df["movie"], df["rating"]))
    
    #ต้องสั่งให้ return df ที่ได้รับการ append 3 columns นี้แล้วด้วย เพราะจะเอาไปใช้เรียกในฟังชั่นถัดไป
    #เรื่องค่าของตัวแปร value vs reference แม่งเรื่องใหญ่เหมือนกันนี่หว่า
    return df["user"], df["movie"], df["rating"]

def train_test_split(prepare_embedding):
    df = raaah().sample(frac=1, random_state=42)
    x = df[["user", "movie"]].values
    # Normalize the targets between 0 and 1. Makes it easy to train.
    y = df["rating"].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
    # Assuming training on 90% of the data and validating on 10%.
    train_indices = int(0.9 * df.shape[0])
    x_train, x_val, y_train, y_val = (x[:train_indices],
                                      x[train_indices:],
                                      y[:train_indices],
                                      y[train_indices:])
    return x_train, x_val, y_train, y_val