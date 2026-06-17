from fastapi import FastAPI
import psycopg2
import pandas as pd

app = FastAPI()

DATABASE_URL = "DATABASE_URL"


@app.get("/")
def home():
    return {"message": "API Works"}


@app.get("/recommendation-data")
def get_data():

    conn = psycopg2.connect(DATABASE_URL)

    places = pd.read_sql(
        "SELECT * FROM recommendation_places",
        conn
    )

    children = pd.read_sql(
        "SELECT * FROM child_places",
        conn
    )

    conn.close()

    # Convert NaN values to None (null in JSON)
    places = places.where(pd.notnull(places), None)
    children = children.where(pd.notnull(children), None)

    return {
        "recommendation_places": places.to_dict(orient="records"),
        "child_places": children.to_dict(orient="records")
    }