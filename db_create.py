import csv
import sqlite3
from datetime import datetime

# Function to convert 'dd/mm/yyyy' to 'yyyy/mm/dd' format
def convert_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        return date_obj.strftime('%Y/%m/%d')
    except ValueError:
        return None

def create_db():
    # Replace with your CSV file name
    csv_file = 'Crash Statistics Victoria.csv'
    # Replace with your desired database name
    database_file = 'Crash Statistics Victoria.db'

    # Create a SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Create a table with 24 columns, including one for the converted date
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
    """)

    # Read the CSV file and insert data into the database
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            original_date = row['ACCIDENT_DATE']  # Replace with the name of your date column
            formatted_date = convert_date(original_date)
            if formatted_date:
                # Remove the date column from the row dictionary
                del row['ACCIDENT_DATE']
                # Add the converted date to the row
                row['ACCIDENT_DATE'] = formatted_date
                # Prepare the SQL INSERT statement dynamically based on the columns
                columns = ', '.join(row.keys())
                placeholders = ', '.join('?' for _ in row)
                query = f'INSERT INTO Crash ({columns}) VALUES ({placeholders})'
                cursor.execute(query, tuple(row.values()))

    # Commit changes and close the database
    conn.commit()
    conn.close()

    # print("Data from the CSV file has been converted and inserted into the database.")
