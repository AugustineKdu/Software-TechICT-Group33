import sqlite3
from collections import defaultdict

def get_data_for_third_graph(start_date, end_date, alcohol_related, category):

    conn = sqlite3.connect(r"Crash Statistics Victoria.db")
    cursor = conn.cursor()

    # Execute an SQL query to retrieve accident data within the specified date range

    query = """
            SELECT ACCIDENT_DATE, ACCIDENT_TYPE, SEVERITY, REGION_NAME FROM Crash WHERE ACCIDENT_DATE BETWEEN ? AND ? AND ALCOHOL_RELATED LIKE ?;
            """
    if alcohol_related == "All":
        parameters_list = (start_date, end_date, "%")
    else:
        parameters_list = (start_date, end_date, f"%{alcohol_related}%")

    cursor.execute(query, parameters_list)

    rows = cursor.fetchall()

    # Create a dictionary to store the count of accidents per month and year
    accident_count_by_month = defaultdict(int)
    accident_count_by_month_line_1 = defaultdict(int)
    accident_count_by_month_line_2 = defaultdict(int)
    accident_count_by_month_line_3 = defaultdict(int)
    accident_count_by_month_line_4 = defaultdict(int)
    accident_count_by_month_line_5 = defaultdict(int)
    accident_count_by_month_line_6 = defaultdict(int)
    accident_count_by_month_line_7 = defaultdict(int)
    accident_count_by_month_line_8 = defaultdict(int)
    accident_count_by_month_line_9 = defaultdict(int)
    ACCIDENT_TYPE = ["Collision with a fixed object", "collision with some other object", "Collision with vehicle", "Fall from or in moving vehicle", 
                     "No collision and no object struck", "Other accident", "Struck animal", "Struck Pedestrian", "Vehicle overturned (no collision)"]
    SEVERITY = ["Fatal accident", "Non injury accident", "Other injury accident", "Serious injury accident"]
    REGION_NAME = ['', 'EASTERN REGION', 'METROPOLITAN NORTH WEST REGION', 'METROPOLITAN SOUTH EAST REGION', 'NORTH EASTERN REGION', 
                   'NORTHERN REGION', 'SOUTH WESTERN REGION', 'WESTERN REGION']

    # Calculate the count of accidents per month and year
    for row in rows:
        year, month, _ = row[0].split('/')
        key = f"{year}/{month}"
        accident_count_by_month[key] += 1

        if category == "ACCIDENT_TYPE":
            label = ACCIDENT_TYPE
            if row[1] == ACCIDENT_TYPE[0]:
                accident_count_by_month_line_1[key] += 1
            elif row[1] == ACCIDENT_TYPE[1]:
                accident_count_by_month_line_2[key] += 1
            elif row[1] == ACCIDENT_TYPE[2]:
                accident_count_by_month_line_3[key] += 1
            elif row[1] == ACCIDENT_TYPE[3]:
                accident_count_by_month_line_4[key] += 1
            elif row[1] == ACCIDENT_TYPE[4]:
                accident_count_by_month_line_5[key] += 1
            elif row[1] == ACCIDENT_TYPE[5]:
                accident_count_by_month_line_6[key] += 1
            elif row[1] == ACCIDENT_TYPE[6]:
                accident_count_by_month_line_7[key] += 1
            elif row[1] == ACCIDENT_TYPE[7]:
                accident_count_by_month_line_8[key] += 1
            elif row[1] == ACCIDENT_TYPE[8]:
                accident_count_by_month_line_9[key] += 1
        elif category == "SEVERITY":
            label = SEVERITY
            if row[2] == SEVERITY[0]:
                accident_count_by_month_line_1[key] += 1
            elif row[2] == SEVERITY[1]:
                accident_count_by_month_line_2[key] += 1
            elif row[2] == SEVERITY[2]:
                accident_count_by_month_line_3[key] += 1
            elif row[2] == SEVERITY[3]:
                accident_count_by_month_line_4[key] += 1
        elif category == "REGION_NAME":
            label = ["No Record"]
            for i in range(1, 8):
                label.append(REGION_NAME[i])

            if row[3] == REGION_NAME[0]:
                accident_count_by_month_line_1[key] += 1
            elif row[3] == REGION_NAME[1]:
                accident_count_by_month_line_2[key] += 1
            elif row[3] == REGION_NAME[2]:
                accident_count_by_month_line_3[key] += 1
            elif row[3] == REGION_NAME[3]:
                accident_count_by_month_line_4[key] += 1
            elif row[3] == REGION_NAME[4]:
                accident_count_by_month_line_5[key] += 1
            elif row[3] == REGION_NAME[5]:
                accident_count_by_month_line_6[key] += 1
            elif row[3] == REGION_NAME[6]:
                accident_count_by_month_line_7[key] += 1
            elif row[3] == REGION_NAME[7]:
                accident_count_by_month_line_8[key] += 1

    # Close the database connection
    conn.close()

    # Extract the keys (month-year) and values (accident counts) from the dictionary
    months = list(accident_count_by_month.keys())
    accident_counts = list(accident_count_by_month.values())

    #Store the data into the line list
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    y6 = []
    y7 = []  
    y8 = []
    y9 = []

    for i in months:
        y1.append(accident_count_by_month_line_1[i])
        y2.append(accident_count_by_month_line_2[i])
        y3.append(accident_count_by_month_line_3[i])
        y4.append(accident_count_by_month_line_4[i])
        y5.append(accident_count_by_month_line_5[i])
        y6.append(accident_count_by_month_line_6[i])
        y7.append(accident_count_by_month_line_7[i])
        y8.append(accident_count_by_month_line_8[i])
        y9.append(accident_count_by_month_line_9[i])

    y = accident_counts
    x = months
    x_count = []
    n = 1
    for i in y:
        n += 1
        x_count.append(n)

    y = [y1, y2, y3, y4, y5, y6, y7, y8, y9]


    return (y, x, x_count, label)


# get_data_for_third_graph("2018/12/01", "2019/01/01", "All", "SEVERITY")
