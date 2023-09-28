import sqlite3
import csv

# Define the database name and CSV file name
database_name = "Crash Statistics Victoria.db"
csv_file = "Crash Statistics Victoria.csv"
table_name = "Crash"

# Connect to the SQLite database
conn = sqlite3.connect(database_name)
cursor = conn.cursor()

# Create a table (adjust column names and data types as needed)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Crash (
        OBJECTID    INTEGER PRIMARY KEY,
        ACCIDENT_NO VARCHAR(255),
        ABS_CODE    VARCHAR(255),
        ACCIDENT_STATUS VARCHAR(10),
        ACCIDENT_DATE   DATE,
        ACCIDENT_TIME   TIME,
        ALCOHOLTIME VARCHAR(5),
        ACCIDENT_TYPE   VARCHAR(255),
        DAY_OF_WEEK VARCHAR(10),
        DCA_CODE    VARCHAR(255),
        HIT_RUN_FLAG    VARCHAR(5),
        LIGHT_CONDITION VARCHAR(50),
        POLICE_ATTEND   VARCHAR(5),
        ROAD_GEOMETRY   VARCHAR(255),
        SEVERITY    VARCHAR(255),
        SPEED_ZONE  VARCHAR(100),
        RUN_OFFROAD VARCHAR(5),
        NODE_ID INTEGER,
        LONGITUDE   FLOAT,
        LATITUDE    FLOAT,
        NODE_TYPE   VARCHAR(30),
        LGA_NAME    VARCHAR(100),
        REGION_NAME VARCHAR(255),
        VICGRID_X   FLOAT,
        VICGRID_Y   FLOAT,
        TOTAL_PERSONS   INTEGER,
        INJ_OR_FATAL    INTEGER,
        FATALITY	INTEGER,
        SERIOUSINJURY	INTEGER,
        OTHERINJURY INTEGER,
        NONINJURED	INTEGER,
        MALES   INTEGER,
        FEMALES INTEGER,
        BICYCLIST	INTEGER,
        PASSENGER	INTEGER,
        DRIVER	INTEGER,
        PEDESTRIAN	INTEGER,
        PILLION	INTEGER,
        MOTORIST    INTEGER,
        UNKNOWN	INTEGER,
        PED_CYCLIST_5_12	INTEGER,
        PED_CYCLIST_13_18	INTEGER,
        OLD_PEDESTRIAN	INTEGER,
        OLD_DRIVER  INTEGER,
        YOUNG_DRIVER	INTEGER,
        ALCOHOL_RELATED	VARCHAR(5),
        UNLICENCSED	INTEGER,
        NO_OF_VEHICLES	INTEGER,
        HEAVYVEHICLE	INTEGER,
        PASSENGERVEHICLE	INTEGER,
        MOTORCYCLE	INTEGER,
        PUBLICVEHICLE	INTEGER,
        DEG_URBAN_NAME	VARCHAR(50),
        DEG_URBAN_ALL	VARCHAR(100),
        LGA_NAME_ALL	VARCHAR(100),
        REGION_NAME_ALL	VARCHAR(255),
        SRNS	VARCHAR(5),
        SRNS_ALL	VARCHAR(10),
        RMA	VARCHAR(30),
        RMA_ALL	VARCHAR(50),
        DIVIDED VARCHAR(15),
        DIVIDED_ALL	VARCHAR(20),
        STAT_DIV_NAME   VARCHAR(20)


    )
""".format(table_name))

# Import data from the CSV file
with open(csv_file, 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row if it exists in the CSV
    for row in csv_reader:
        # cursor.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)  # Adjust column count as needed
        cursor.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)  # Adjust column count as needed
# Commit changes and close the database connection
conn.commit()
conn.close()

print(f"Data from '{csv_file}' has been imported into '{table_name}' in '{database_name}'.")
