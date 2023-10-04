import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from code_line_graph import get_avgAccident
import numpy as np


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

# Create the frames
first_frame = tk.Frame(root)
first_frame.pack(fill='x')

second_frame = tk.Frame(root)
second_frame.pack(fill='both', expand=True)

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
alcohol_related_combobox = ttk.Combobox(
    first_frame, values=alcohol_related_options, state="readonly")
alcohol_related_combobox.set("All")
alcohol_related_combobox.grid(
    row=0, column=5, padx=(0, 10), pady=10, sticky='w')

# Accident Type Label and Combobox
accident_type_label = tk.Label(first_frame, text="Accident Type:")
accident_type_label.grid(row=0, column=6, padx=(10, 0), pady=10, sticky='e')

accident_type_options = ["All", "Collision with a fixed object", "collision with some other object", "Collision with vehicle", "Fall from or in moving vehicle",
                         "No collision and no object struck", "Other accident", "Struck animal", "Struck Pedestrian", "Vehicle overturned (no collision)"]
accident_type_combobox = ttk.Combobox(
    first_frame, values=accident_type_options, state="readonly")
accident_type_combobox.set("All")
accident_type_combobox.grid(row=0, column=7, padx=(0, 10), pady=10, sticky='w')

# Define the search button


def search_by_date_and_type():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    alcohol_related = alcohol_related_combobox.get()
    accident_type = accident_type_combobox.get()

    display_line_graph(start_date, end_date)



search_button = tk.Button(first_frame, text="Search",
                          command=search_by_date_and_type)
search_button.grid(row=1, column=8, padx=10, pady=10, sticky='e')


# Function for display average number of accident by hourly
def display_line_graph(start_date, end_date):
        hour = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10', '10-11', 
        '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-24']

        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot([i for i in range(0, 24)], get_avgAccident(start_date, end_date), color="blue", linewidth=2.5, linestyle="-")
        ax.set(title='Average Number of Accidents Per Hour',
                xlabel='Time (Hourly)', ylabel='Number of Accidents')
        ax.set_xticks([i for i in range(0, 24)])
        ax.set_xticklabels(hour, fontsize=7, rotation=5)
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=second_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, padx=10, pady=10)
        canvas.draw()

# Run the Tkinter event loop
root.mainloop()


