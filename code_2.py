import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from first_graph import get_avgAccident
from second_graph import get_data_for_second_graph


conn = sqlite3.connect("Crash Statistics Victoria.db")
cursor = conn.cursor()
cursor.execute("SELECT min(ACCIDENT_DATE), max(ACCIDENT_DATE) FROM Crash")
data = cursor.fetchone()
min_date = data[0]
max_date = data[-1]
conn.close()

# Create the main window
root = tk.Tk()
root.title("Accident Analysis")

# first frame for search function
first_frame = tk.Frame(root)
first_frame.pack(fill='x')

# second frame for display graph
second_frame = tk.Frame(root)
second_frame.pack(fill='both', expand=True)

# third frame for display table 
frame3 = tk.Frame(root)
frame3.pack(side=tk.TOP)

tree = ttk.Treeview(frame3, columns=("OBJECTID", "ACCIDENT_NO", "ACCIDENT_DATE", "ACCIDENT_TIME", "ALCOHOL_RELATED", 
                                     "ACCIDENT_TYPE", "SEVERITY", "REGION_NAME"), show="headings")

# Define the first frame components
start_date_label = tk.Label(first_frame, text="Start Date:")
start_date_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

start_date_entry = tk.Entry(first_frame)
start_date_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

end_date_label = tk.Label(first_frame, text="End Date:")
end_date_label.grid(row=0, column=2, padx=10, pady=10, sticky='w')

end_date_entry = tk.Entry(first_frame)
end_date_entry.grid(row=0, column=3, padx=10, pady=10, sticky='w')

# Add a label to display the selectable date range
date_range_label = tk.Label(
    first_frame, text=f"Selectable Date Range: {min_date} to {max_date}", font=('Arial', 9), fg='grey')
date_range_label.grid(row=1, column=0, columnspan=4, pady=(0, 10))

# Alcohol Related Label and Combobox
alcohol_related_label = tk.Label(first_frame, text="Alcohol Related:")
alcohol_related_label.grid(row=0, column=4, padx=(10, 0), pady=10, sticky='e')

alcohol_related_options = ["All", "Yes", "No"]
alcohol_related_combobox = ttk.Combobox(first_frame, values=alcohol_related_options, state="readonly")
alcohol_related_combobox.set("All")
alcohol_related_combobox.grid(row=0, column=5, padx=(0, 10), pady=10, sticky='w')

# Accident Type Label and Combobox
accident_type_label = tk.Label(first_frame, text="Accident Type:")
accident_type_label.grid(row=0, column=6, padx=(10, 0), pady=10, sticky='e')

accident_type_options = ["All", "Collision with a fixed object", "collision with some other object", "Collision with vehicle", 
                         "Fall from or in moving vehicle", "No collision and no object struck", "Other accident", "Struck animal", 
                         "Struck Pedestrian", "Vehicle overturned (no collision)"]
accident_type_combobox = ttk.Combobox(first_frame, values=accident_type_options, state="readonly")
accident_type_combobox.set("All")
accident_type_combobox.grid(row=0, column=7, padx=(0, 10), pady=10, sticky='w')

# Define the search button
def search_by_date_and_type():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    alcohol_related = alcohol_related_combobox.get()
    accident_type = accident_type_combobox.get()

    if start_date < min_date or end_date > max_date:
        messagebox.showerror(
            "Invalid Date", "Please enter a valid date in YYYY/MM/DD format.")
    else:
        display_line_graph(start_date, end_date)
        fetch_data_and_display_table(start_date, end_date, alcohol_related)



search_button = tk.Button(first_frame, text="Search", command=search_by_date_and_type)
search_button.grid(row=1, column=8, padx=10, pady=10, sticky='e')

    
# Function for display average number of accident by hourly
def display_line_graph(start_date, end_date):
    hour = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10', '10-11', '11-12', '12-13', '13-14',
            '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-24']

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 6))
    ax1.plot([i for i in range(0, 24)], get_avgAccident(start_date, end_date), color="blue", linewidth=2.5, linestyle="-")
    ax1.set(title=f'Average Number of Accidents Per Hour from {start_date} to {end_date}', xlabel='Time (Hourly)', ylabel='Number of Accidents')
    ax1.set_xticks([i for i in range(0, 24)])
    ax1.set_xticklabels(hour, fontsize=7)
    ax1.grid(False)

    axis = get_data_for_second_graph(start_date, end_date)
    # ax2.plot(axis[-1], axis[0], color="green", linewidth=2.5, linestyle="-")
    ax2.bar(axis[-1], axis[0], color="green", width = 0.1)
    ax2.set(title=f'The Number of Accidents For Each Region from {start_date} to {end_date}', xlabel='Region', ylabel='Number of Accidents')
    ax2.set_xticks(axis[-1])
    ax2.set_xticklabels(axis[1], fontsize=7, rotation=5)
    ax2.grid(False)

    month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    ax3.plot([i for i in range(0, 12)], [i for i in range(12, 0, -1)], color="green", linewidth=2.5, linestyle="-")
    ax3.set(title=f'The Number of Accidents For Each Region from {start_date} to {end_date}', xlabel='Region', ylabel='Number of Accidents')
    ax3.set_xticks([i for i in range(0, 12)])
    ax3.set_xticklabels(month, fontsize=7, rotation=5)
    ax3.grid(False)

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=second_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, padx=10, pady=10)
    canvas.draw()



# function for display table
def fetch_data_and_display_table(start_date, end_date, alcohol_related):

    conn = sqlite3.connect('Crash Statistics Victoria.db')
    cursor = conn.cursor()
    # Execute a SQL query to fetch data (replace 'your_table' with your actual table name)
    if alcohol_related == "No":
        query = """
                SELECT OBJECTID, ACCIDENT_NO, ACCIDENT_DATE, ACCIDENT_TIME, ALCOHOL_RELATED, ACCIDENT_TYPE, SEVERITY, REGION_NAME 
                FROM Crash WHERE ACCIDENT_DATE BETWEEN ? AND ? AND ALCOHOL_RELATED = 'No';
                """
    elif alcohol_related == "Yes":
        query = """
                SELECT OBJECTID, ACCIDENT_NO, ACCIDENT_DATE, ACCIDENT_TIME, ALCOHOL_RELATED, ACCIDENT_TYPE, SEVERITY, REGION_NAME 
                FROM Crash WHERE ACCIDENT_DATE BETWEEN ? AND ? AND ALCOHOL_RELATED = 'Yes';
                """
    else:
        query = """
                SELECT OBJECTID, ACCIDENT_NO, ACCIDENT_DATE, ACCIDENT_TIME, ALCOHOL_RELATED, ACCIDENT_TYPE, SEVERITY, REGION_NAME 
                FROM Crash WHERE ACCIDENT_DATE BETWEEN ? AND ?;
                """
    cursor.execute(query, (start_date, end_date))
    rows = cursor.fetchall()

    # Clear existing data in the table (if any)
    for row in tree.get_children():
        tree.delete(row)

    # Insert fetched data into the table
    for row in rows:
        tree.insert('', 'end', values=row)

    # Close the database connection
    conn.close()

    tree.heading("#1", text="OBJECTID")
    tree.heading("#2", text="ACCIDENT_NO")
    tree.heading("#3", text="ACCIDENT_DATE")
    tree.heading("#4", text="ACCIDENT_TIME")
    tree.heading("#5", text="ALCOHOL_RELATED")
    tree.heading("#6", text="ACCIDENT_TYPE")
    tree.heading("#7", text="SEVERITY")
    tree.heading("#8", text="REGION_NAME")

    tree.column("#0", width=0, anchor="center")
    tree.column("#1", width=80, anchor="center")
    tree.column("#2", width=110, anchor="center")
    tree.column("#3", width=100, anchor="center")
    tree.column("#4", width=100, anchor="center")
    tree.column("#5", width=120, anchor="center")
    tree.column("#6", width=270, anchor="center")
    tree.column("#7", width=180, anchor="center")
    tree.column("#8", width=300, anchor="center")

    tree.pack()

    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)



# Run the Tkinter event loop
root.mainloop()


