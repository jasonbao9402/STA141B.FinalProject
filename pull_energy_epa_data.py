import pandas as pd
import requests
import json


# read your api key from file

def read_key(keyfile):
    with open(keyfile) as f:
        return f.readline().strip("\n")
# fill with your api key location
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

    renewable_energy["generation"] = renewable_energy["generation"].fillna(0)
    renewable_energy["period"] = renewable_energy["period"].fillna(0)

    renewable_energy = renewable_energy.rename(columns={
        "location": "state",
        "period": "date",
        "fuelTypeDescription": "renewable_energy_type",
        "sectorDescription": "renewable_energy_sector",
        "generation": "renewable_energy_output"
    })

    renewable_energy = renewable_energy[[
        "state",
        "date",
        "renewable_energy_type",
        "renewable_energy_sector",
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

    # change numeric values from string to int
    carbon_emissions["value"] = pd.to_numeric(carbon_emissions["value"], errors = "coerce")
    carbon_emissions["period"] = pd.to_numeric(carbon_emissions["period"])
    
    # fill null values with 0
    carbon_emissions["value"] = carbon_emissions["value"].fillna(0)
    carbon_emissions["period"] = carbon_emissions["period"].fillna(0)

    carbon_emissions = carbon_emissions.rename(columns={
        "stateId": "state",
        "period": "date",
        "sector-name": "carbon_emissions_sector",
        "value": "carbon_emissions_value"
    })

    carbon_emissions = carbon_emissions[[
        "state",
        "date",
        "carbon_emissions_sector",
        "carbon_emissions_value"
    ]]

    return carbon_emissions

    #original columns: 'period', 'sectorId', 'sector-name', 'fuelId', 'fuel-name', 'stateId', 'state-name', 'value', 'value-units'


# API pull for state policy

def state_policy_pull():
    policy_cols = [
        "state_firm",
        "year",
        "rps_enact",
        "rps_eff",
        "rps_plant",
        "rps_noplant",
        "deregulation",
        "disc_enact",
        "disc_eff",
        "green_policy_en",
    ]

    policy_df = pd.read_csv(
        "energy_policy_dataset/utwind09_14_09b_labels_stata.csv",
        usecols=policy_cols
    )

    policy_df = policy_df.rename(columns={"state_firm": "state", "year": "date"})

    numeric_cols = [c for c in policy_df.columns if c not in ["state", "date"]]
    for c in numeric_cols:
        policy_df[c] = pd.to_numeric(policy_df[c], errors="coerce")

    policy_cols_binary = [
        "rps_enact",
        "rps_eff",
        "rps_plant",
        "rps_noplant",
        "deregulation",
        "disc_enact",
        "disc_eff",
        "green_policy_en",
    ]
    policy_cont_cols = [c for c in numeric_cols if c not in policy_cols_binary]

    agg_map = {c: "max" for c in policy_cols_binary}
    agg_map.update({c: "mean" for c in policy_cont_cols})

    state_policy = (
        policy_df.groupby(["state", "date"], as_index=False)
        .agg(agg_map)
        .sort_values(["state", "date"])
    )

    return state_policy
