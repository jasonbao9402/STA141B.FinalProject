import sqlite3 as sql
from extract_eia import renewable_energy_pull, carbon_emissions_pull

# Create dataframes from extract_eia.py
carbon_emissions = carbon_emissions_pull()
renewable_energy = renewable_energy_pull()

# Use dataframes to fill tables in database
def load_table(df, table_name):
    conn = sql.connect(".../Energy_Data.db")
    df.to_sql(table_name, conn, if_exists = "replace", index = False)
    conn.close()

load_table(carbon_emissions, "carbon_emissions")
load_table(renewable_energy, "renewable_energy")

