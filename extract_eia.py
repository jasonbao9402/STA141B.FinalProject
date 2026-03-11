import pandas as pd
import requests
import json


# read your api key from file

def read_key(keyfile):
    with open(keyfile) as f:
        return f.readline().strip("\n")
key = read_key("../eia_key.txt") 


# API pull for carbon emissions from eia website

emission_url = f"https://api.eia.gov/v2/co2-emissions/co2-emissions-aggregates/data/?api_key={key}"
params = {
    "frequency": "annual",
    "data": [
        "value"
    ],
    "facets": {},
    "start": "2001",
    "end": "2010",
    "sort": [
        {
            "column": "period",
            "direction": "desc"
        }
    ],
    "offset": 0,
    "length": 5000
}
headers = {
    "X-Params": json.dumps(params)
}

emission_response = requests.get(url, headers = headers)


# conversion of carbon emission data to data frame

rows = emission_response.json()["response"]["data"]

carbon_emissions = pd.DataFrame(rows)

carbon_emissions["value"] = pd.to_numeric(carbon_emissions["value"], errors = "coerce")
carbon_emissions["period"] = pd.to_numeric(carbon_emissions["period"])

carbon_emissions = carbon_emissions.rename(columns={
    "state-name": "state",
    "period": "date",
    "sector-name": "carbon_emissions_type",
    "value": "carbon_emissions_value"
})

carbon_emissions = carbon_emissions[[
    "state",
    "date",
    "carbon_emissions_type",
    "carbon_emissions_value"
]]

#print(carbon_emissions.columns.tolist())
#print(carbon_emissions.head())

#original columns: 'period', 'sectorId', 'sector-name', 'fuelId', 'fuel-name', 'stateId', 'state-name', 'value', 'value-units'


# API pull for renewable energy

renewables_url = f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?api_key={key}"
params = {
    "frequency": "annual",
    "data": [
        "generation"
    ],
    "facets": {
        "fueltypeid": [
            "AOR",
            "REN",
            "SPV",
            "STH",
            "SUN",
            "WAS",
            "WND",
            "WNT"
        ]
    },
    "start": "2001",
    "end": "2010",
    "sort": [
        {
            "column": "period",
            "direction": "desc"
        }
    ],
    "offset": 0,
    "length": 5000
}

headers = {
    "X-Params": json.dumps(params)
}

renewables_response = requests.get(url, headers = headers)


# conversion of renewable energy data to data frame

rows = renewables_response.json()["response"]["data"]
renewable_energy = pd.DataFrame(rows)

renewable_energy["generation"] = pd.to_numeric(renewable_energy["generation"], errors = "coerce")
renewable_energy["period"] = pd.to_numeric(renewable_energy["period"])

renewable_energy = renewable_energy.rename(columns={
    "location": "state",
    "period": "date",
    "fuelTypeDescription": "renewable_energy_type",
    "generation": "renewable_energy_output"
})

renewable_energy = renewable_energy[[
    "state",
    "date",
    "renewable_energy_type",
    "renewable_energy_output"
]]

#print(renewable_energy.columns.tolist())
#print(renewable_energy.head())

# original columns: 'period', 'location', 'stateDescription', 'sectorid', 'sectorDescription', 'fueltypeid', 'fuelTypeDescription', 'generation', 'generation-units'
