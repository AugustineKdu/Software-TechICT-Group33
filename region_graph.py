import sqlite3
import matplotlib.pyplot as plt

def get_Axis_for_region_graph(start_date, end_date):
    accident = []
    region = []
    
    connection = sqlite3.connect(r"Crash Statistics Victoria.db")
    cursor = connection.cursor()
    query = """
            SELECT REGION_NAME, COUNT() as Number_of_Accident FROM Crash WHERE ACCIDENT_DATE BETWEEN ? AND ? GROUP BY REGION_NAME;
            """
    
    parameters_list = (start_date, end_date)
    cursor.execute(query, parameters_list)
    
    results = cursor.fetchall()

    for r in results:
        if r[0] == " ":
             region.append("No record")
             accident.append(r[1])
        else:
             region.append(r[0])
             accident.append(r[1])
    count = []
    n = 1
    for i in accident:
         n += 1
         count.append(n)

    return (accident, region, count)


# "No Record", "EASTERN REGION", "METROPOLITAN NORTH WEST REGION", "METROPOLITAN SOUTH EAST REGION", "NORTH EASTERN REGION", "NORTHERN REGION", "SOUTH WESTERN REGION", "WESTERN REGION"

