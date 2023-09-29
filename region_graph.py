import sqlite3
import matplotlib.pyplot as plt

start_date = input("start date (yyyy/mm/dd): ")
end_date = input("end date (yyyy/mm/dd): ")

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

        
plt.figure(figsize=(16, 5))
plt.plot(region, accident, color="green", linewidth=2.5, linestyle="-") 
plt.title("Total Number of Accidents in Region") 
plt.ylabel("Number of Accident") 
plt.xlabel("Region") 
plt.xticks(fontsize=7, rotation=5)
plt.show()
