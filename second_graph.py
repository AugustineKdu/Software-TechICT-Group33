import sqlite3

def get_data_for_second_graph(start_date, end_date, alcohol_related, category):
    y = []
    x = []
    
    connection = sqlite3.connect(r"Crash Statistics Victoria.db")
    cursor = connection.cursor()
    if category == "ACCIDENT_TYPE":
       query = """
               SELECT ACCIDENT_TYPE, COUNT() as Number_of_Accident FROM Crash WHERE ACCIDENT_DATE BETWEEN ? AND ? AND ALCOHOL_RELATED LIKE ? GROUP BY ACCIDENT_TYPE;
               """
    elif category == "SEVERITY":
       query = """
               SELECT SEVERITY, COUNT() as Number_of_Accident FROM Crash WHERE ACCIDENT_DATE BETWEEN ? AND ? AND ALCOHOL_RELATED LIKE ? GROUP BY SEVERITY;
               """
    elif category == "REGION_NAME":
       query = """
               SELECT REGION_NAME, COUNT() as Number_of_Accident FROM Crash WHERE ACCIDENT_DATE BETWEEN ? AND ? AND ALCOHOL_RELATED LIKE ? GROUP BY REGION_NAME;
               """
       
    if alcohol_related == "All":
        parameters_list = (start_date, end_date, "%")
    else:
        parameters_list = (start_date, end_date, f"%{alcohol_related}%")
    cursor.execute(query, parameters_list)
    
    results = cursor.fetchall()

    for r in results:
        if r[0] == " ":
             x.append("No record")
             y.append(r[1])
        else:
             x.append(r[0])
             y.append(r[1])
    x_count = []
    n = 1
    for i in y:
         n += 1
         x_count.append(n)

    return (y, x, x_count)


# get_data_for_second_graph("2013/07/01", "2019/03/21", "All", "REGION_NAME")