import sqlite3
import tkinter as tk
from tkinter import ttk

start_date = input("start date (yyyy/mm/dd): ")
end_date = input("end date (yyyy/mm/dd): ")


conn = sqlite3.connect(r"Crash Statistics Victoria.db")
cursor = conn.cursor()

# Function to fetch data from the SQLite database
def fetch_data():

    # Replace 'your_table_name' with the actual name of your table
    query = "SELECT OBJECTID, ACCIDENT_NO, ACCIDENT_DATE, ACCIDENT_TIME, ALCOHOL_RELATED, ACCIDENT_TYPE, SEVERITY, REGION_NAME FROM Crash WHERE ACCIDENT_DATE BETWEEN ? AND ?;"
    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchall()
    
    return data


# Create a Tkinter window
root = tk.Tk()
root.title("Scrollable Table")

# Create a scrollable frame
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Fetch data from the database
data = fetch_data()

# Display the data in a table
if data:
    columns = [description[0] for description in cursor.description]


    for i, col in enumerate(columns):
        ttk.Label(frame, text=col, borderwidth=1, relief="solid").grid(row=0, column=i, sticky="nsew")

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            ttk.Label(frame, text=val, borderwidth=1, relief="solid").grid(row=i + 1, column=j, sticky="nsew")

    # Configure column weights and row weights
    for i in range(len(columns)):
        frame.grid_columnconfigure(i, weight=1)

    for i in range(len(data) + 1):
        frame.grid_rowconfigure(i, weight=1)
else:
    ttk.Label(frame, text="No data found", borderwidth=1, relief="solid").grid(row=0, column=0, sticky="nsew")


conn.close()
# Start the Tkinter main loop
root.mainloop()





