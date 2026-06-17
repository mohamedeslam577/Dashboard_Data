from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import pandas as pd
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql://postgres:YqavFXcTXlyBuMNKTWObIkZeiGodEuiA@kodama.proxy.rlwy.net:26773/railway"


@app.get("/")
def home():
    return {"message": "API Works"}


@app.get("/recommendation-data")
def get_data():

    conn = psycopg2.connect(DATABASE_URL)

    places = pd.read_sql("SELECT * FROM recommendation_places", conn)
    children = pd.read_sql("SELECT * FROM child_places", conn)

    conn.close()

    # Replace ALL NaN/NaT/inf values with None before serializing
    places = places.replace({np.nan: None, np.inf: None, -np.inf: None})
    children = children.replace({np.nan: None, np.inf: None, -np.inf: None})

    # Convert object columns: any remaining float NaN wrapped in objects
    def clean_records(df):
        records = df.to_dict(orient="records")
        return [
            {
                k: (None if isinstance(v, float) and (v != v) else v)
                for k, v in row.items()
            }
            for row in records
        ]

    return {
        "recommendation_places": clean_records(places),
        "child_places": clean_records(children),
    }