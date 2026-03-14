from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv() # load the .env file
EIA_API_KEY = os.getenv("EIA_API_KEY")

url = f"https://api.eia.gov/v2/seds/data?api_key={EIA_API_KEY}"

params = {
    "frequency": "annual",
    "data[]": "value",
    "start": "1970",
    "end": "2024",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "offset": 0,
    "length": 5000
}

response = requests.get(url, params=params)

print(response.status_code)

print(response.json())
