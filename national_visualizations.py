import sqlite3 as sql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# setup
path_db = "Downloads/Energy_Data.db"
db = sql.connect(path_db)

sns.set_theme(style="white", palette="Set2")
plt.rcParams["figure.figsize"] = [8, 5]

# national totals
totals_query = """
WITH renewable_totals AS (
    SELECT
        date,
        SUM(renewable_energy_output) AS total_renewables
    FROM renewable_energy
    GROUP BY date
),
emissions_totals AS (
    SELECT
        date,
        SUM(carbon_emissions_value) AS total_emissions
    FROM carbon_emissions
    GROUP BY date
)
SELECT
    r.date,
    r.total_renewables,
    e.total_emissions
FROM renewable_totals r
JOIN emissions_totals e
ON r.date = e.date
ORDER BY r.date
"""

df = pd.read_sql(totals_query, db)

# renewable generation by type
type_query = """
SELECT
    date,
    renewable_energy_type,
    SUM(renewable_energy_output) AS total_output
FROM renewable_energy
GROUP BY date, renewable_energy_type
ORDER BY date, renewable_energy_type
"""

type_df = pd.read_sql(type_query, db)

# renewable generation by sector
renew_sector_query = """
SELECT
    date,
    renewable_energy_sector,
    SUM(renewable_energy_output) AS total_output
FROM renewable_energy
GROUP BY date, renewable_energy_sector
ORDER BY date, renewable_energy_sector
"""

renew_sector_df = pd.read_sql(renew_sector_query, db)

# carbon emissions by sector
emissions_sector_query = """
SELECT
    date,
    carbon_emissions_sector,
    SUM(carbon_emissions_value) AS total_emissions
FROM carbon_emissions
GROUP BY date, carbon_emissions_sector
ORDER BY date, carbon_emissions_sector
"""

emissions_sector_df = pd.read_sql(emissions_sector_query, db)

db.close()

# filter renewable types
allowed_types = [
    "wind",
    "solar",
    "all renewables",
    "total renewables",
    "total renewable energy"
]

type_df["renewable_energy_type_lower"] = type_df["renewable_energy_type"].str.lower()
type_df = type_df[type_df["renewable_energy_type_lower"].isin(allowed_types)].copy()

type_df["renewable_energy_type"] = type_df["renewable_energy_type_lower"]

df["renewables_million_mwh"] = df["total_renewables"] / 1e6
type_df["total_output_million"] = type_df["total_output"] / 1e6
renew_sector_df["total_output_million"] = renew_sector_df["total_output"] / 1e6

df["renewables_index"] = df["renewables_million_mwh"] / df["renewables_million_mwh"].iloc[0] * 100
df["emissions_index"] = df["total_emissions"] / df["total_emissions"].iloc[0] * 100

df["renewables_change"] = df["renewables_million_mwh"].diff()
df["emissions_change"] = df["total_emissions"].diff()

df_2005 = df[df["date"] == 2005]

# national renewables
ax = sns.lineplot(data=df, x="date", y="renewables_million_mwh")
plt.axvline(x=2005, linestyle=":", linewidth=1, color="red", label="2005")
ax.set_title("US Renewable Electricity Generation")
ax.set_xlabel("Year")
ax.set_ylabel("Renewable Electricity Generation (Million MWh)")
ax.legend(loc="best")
plt.show()
plt.savefig("national_renewables.png")
plt.close()

# national emissions
ax = sns.lineplot(data=df, x="date", y="total_emissions")
plt.axvline(x=2005, linestyle=":", linewidth=1, color="red", label="2005")
ax.set_title("US CO2 Emissions")
ax.set_xlabel("Year")
ax.set_ylabel("CO2 Emissions (Million Metric Tons)")
ax.legend(loc="best")
plt.show()
plt.savefig("national_emissions.png")
plt.close()

# renewable generation by selected type
ax = sns.lineplot(
    data=type_df,
    x="date",
    y="total_output_million",
    hue="renewable_energy_type"
)
plt.axvline(x=2005, linestyle=":", linewidth=1, color="red")
ax.set_title("US Renewable Electricity Generation by Type")
ax.set_xlabel("Year")
ax.set_ylabel("Renewable Electricity Generation (Million MWh)")
plt.show()
plt.savefig("national_renewable_type.png")
plt.close()

# renewable generation by sector
ax = sns.lineplot(
    data=renew_sector_df,
    x="date",
    y="total_output_million",
    hue="renewable_energy_sector"
)
plt.axvline(x=2005, linestyle=":", linewidth=1, color="red")
ax.set_title("US Renewable Electricity Generation by Sector")
ax.set_xlabel("Year")
ax.set_ylabel("Renewable Electricity Generation (Million MWh)")
plt.show()
plt.savefig("national_renewable_sector.png")
plt.close()

# carbon emissions by sector
ax = sns.lineplot(
    data=emissions_sector_df,
    x="date",
    y="total_emissions",
    hue="carbon_emissions_sector"
)
plt.axvline(x=2005, linestyle=":", linewidth=1, color="red")
ax.set_title("US CO2 Emissions by Sector")
ax.set_xlabel("Year")
ax.set_ylabel("CO2 Emissions (Million Metric Tons)")
plt.show()
plt.savefig("national_emissions_sector.png")
plt.close()

# relationship: fitted-line plot
lm = sns.lmplot(
    data=df,
    x="renewables_million_mwh",
    y="total_emissions",
    height=5,
    aspect=1.2
)
plt.title("US Renewable Generation vs CO2 Emissions with Best-Fit Line")
plt.xlabel("Renewable Electricity Generation (Million MWh)")
plt.ylabel("CO2 Emissions (Million Metric Tons)")
plt.show()
plt.savefig("national_fitted.png")
plt.close()

