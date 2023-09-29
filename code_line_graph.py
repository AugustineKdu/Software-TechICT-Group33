import sqlite3
import time

start_date = input("start date (yyyy/mm/dd): ")
end_date = input("end date (yyyy/mm/dd): ")

avg_accident = []
hour = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10', '10-11', 
        '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-24']


def days_between_dates(dt1, dt2):
	date_format = "%Y/%m/%d"
	a = time.mktime(time.strptime(dt1, date_format))
	b = time.mktime(time.strptime(dt2, date_format))
	delta = b - a
	return int(delta / 86400 + 1)


# print(days_between_dates(start_date, end_date))

connection = sqlite3.connect(r"Crash Statistics Victoria.db")
cursor = connection.cursor()
queries = [
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '00.00.00' AND '00.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '01.00.00' AND '01.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '02.00.00' AND '02.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '03.00.00' AND '03.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '04.00.00' AND '04.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '05.00.00' AND '05.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '06.00.00' AND '06.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '07.00.00' AND '07.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '08.00.00' AND '08.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '09.00.00' AND '09.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '10.00.00' AND '10.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '11.00.00' AND '11.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '12.00.00' AND '12.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '13.00.00' AND '13.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '14.00.00' AND '14.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '15.00.00' AND '15.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '16.00.00' AND '16.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '17.00.00' AND '17.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '18.00.00' AND '18.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '19.00.00' AND '19.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '20.00.00' AND '20.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '21.00.00' AND '21.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '22.00.00' AND '22.59.59';",
"select count() from Crash where ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TIME BETWEEN '23.00.00' AND '23.59.59';",
]

parameters_list = (start_date, end_date)

for i, query in enumerate(queries):
    cursor.execute(query, parameters_list)

    # Fetch and process the results
    results = cursor.fetchall()
    for r in results:
        total_accidents = int(r[0])
        avg_accident.append((round(total_accidents / (days_between_dates(start_date, end_date)),2)))
print(avg_accident)

        

import matplotlib.pyplot as plt
import numpy as np

x = np.array(avg_accident)
y = np.array(hour)

plt.figure(figsize=(16, 5))
plt.plot(y, x, color="blue", linewidth=2.5, linestyle="-") 
plt.title("Average Number of Accidents Per Hour") 
plt.ylabel("Number of Accident") 
plt.xlabel("Time (Hourly)") 
plt.xticks(fontsize=7, rotation=5)
plt.show()




