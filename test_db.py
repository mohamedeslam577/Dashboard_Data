from fastapi import FastAPI
import psycopg2
import pandas as pd
import os


app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

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

    return {
        "recommendation_places": places.to_dict(orient="records"),
        "child_places": children.to_dict(orient="records")
    }