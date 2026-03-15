import sqlite3 as sql
from pull_energy_epa_data import renewable_energy_pull, carbon_emissions_pull, state_policy_pull

# Create dataframes from extract_eia.py
carbon_emissions = carbon_emissions_pull()
renewable_energy = renewable_energy_pull()
state_policy = state_policy_pull()

# Use dataframes to fill tables in database
def load_table(df, table_name):
    # fill with your database location
    conn = sql.connect("Database/Energy_Data.db")
    df.to_sql(table_name, conn, if_exists = "replace", index = False)
    conn.close()

load_table(carbon_emissions, "carbon_emissions")
load_table(renewable_energy, "renewable_energy")
load_table(state_policy, "state_policy")

print(state_policy)