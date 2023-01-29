import fastapi
import pandas as pd
import numpy as np

app = fastapi.FastAPI()

@app.get("/data")
def read_data():
    # Read the CSV file
    df = pd.read_csv("../MovieSummaries/movies.csv", sep=';')

    df = df.fillna(np.nan)
    # Convert the dataframe to a dictionary
    data = df.to_dict()

    return data
