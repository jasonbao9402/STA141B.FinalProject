import pandas as pd
import requests
import json


# read your api key from file

def read_key(keyfile):
    with open(keyfile) as f:
        return f.readline().strip("\n")
key = read_key("Desktop/eia_key.txt") 


# API pull for renewable energy

def renewable_energy_pull():
    all_rows = []
    offset = 0
    renewables_url = f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?api_key={key}"
    while True:
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
                    "direction": "asc"
                }
            ],
            "offset": offset,
            "length": 5000
        }

        headers = {"X-Params": json.dumps(params)}

        renewables_response = requests.get(renewables_url, headers = headers)

        rows = renewables_response.json()["response"]["data"]
        all_rows.extend(rows)
        offset += 5000
        if len(rows) < 5000:
            break

    # conversion of renewable energy data to data frame

    renewable_energy = pd.DataFrame(all_rows)

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

    return renewable_energy
    # original columns: 'period', 'location', 'stateDescription', 'sectorid', 'sectorDescription', 'fueltypeid', 'fuelTypeDescription', 'generation', 'generation-units'


# API pull for carbon emissions from eia website

def carbon_emissions_pull():
    all_rows = []
    offset = 0
    emission_url = f"https://api.eia.gov/v2/co2-emissions/co2-emissions-aggregates/data/?api_key={key}"
    while True:
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
                    "direction": "asc"
                }
            ],
            "offset": offset,
            "length": 5000
        }
        headers = {"X-Params": json.dumps(params)}

        emission_response = requests.get(emission_url, headers = headers)

        rows = emission_response.json()["response"]["data"]
        all_rows.extend(rows)
        offset += 5000
        if len(rows) < 5000:
            break

    # conversion of carbon emission data to data frame

    carbon_emissions = pd.DataFrame(all_rows)

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

    return carbon_emissions

    #original columns: 'period', 'sectorId', 'sector-name', 'fuelId', 'fuel-name', 'stateId', 'state-name', 'value', 'value-units'


# API pull for state policy

def state_policy_pull():
    policy_url = ""

