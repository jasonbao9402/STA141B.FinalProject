"""
This script initializes the SQLite database and creates the necessary tables for the project.
All workflow follows the official sqllite3 documentation and lecture files

Note: In order to connect to the database from the command-line, do sqlite3 Database/Energy_Data.db
"""

import sqlite3 as db

# create tables for different data sources/sets

create_tables = [
    """CREATE TABLE IF NOT EXISTS renewable_energy 
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            date DATE NOT NULL,
            renewable_energy_type TEXT NOT NULL,
            renewable_energy_sector TEXT NOT NULL,
            renewable_energy_output INT NOT NULL
        );
    """,

    """CREATE TABLE IF NOT EXISTS carbon_emissions
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            date DATE NOT NULL,
            carbon_emissions_sector TEXT NOT NULL,
            carbon_emissions_value REAL NOT NULL
        );
    """,

    """CREATE TABLE IF NOT EXISTS state_policy
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            date DATE NOT NULL,
            rps_enact REAL,
            rps_eff REAL,
            rps_plant REAL,
            rps_noplant REAL,
            deregulation REAL,
            disc_enact REAL,
            disc_eff REAL,
            green_policy_en REAL
        );
    """ 
]

# connect to database or create it if it doesn't exist and create tables
try:
    with db.connect('Database/Energy_Data.db') as conn:
        print(f"SQLite database with version {db.sqlite_version} connected successfully. ")
        cursor = conn.cursor()
        for table in create_tables:
            cursor.execute(table)
        conn.commit()
        print("Tables created successfully.")

except db.OperationalError as e:
    print(f"SQLite database connection failed: {e}")
