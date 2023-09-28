import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the data
file_path = 'Crash Statistics Victoria.csv'
data = pd.read_csv(file_path, parse_dates=['ACCIDENT_DATE'], dayfirst=True)
min_date = data['ACCIDENT_DATE'].min().strftime('%Y-%m-%d')
max_date = data['ACCIDENT_DATE'].max().strftime('%Y-%m-%d')

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
start_date_entry.insert(0, min_date)

end_date_label = tk.Label(first_frame, text="End Date:")
end_date_label.grid(row=0, column=2, padx=10, pady=10, sticky='w')

end_date_entry = tk.Entry(first_frame)
end_date_entry.grid(row=0, column=3, padx=10, pady=10, sticky='w')
end_date_entry.insert(0, max_date)

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

    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
        for widget in second_frame.winfo_children():
            widget.destroy()
        plot_accidents_by_date_and_type(
            start_date, end_date, alcohol_related, accident_type)
    except ValueError:
        messagebox.showerror(
            "Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")


search_button = tk.Button(first_frame, text="Search",
                          command=search_by_date_and_type)
search_button.grid(row=1, column=8, padx=10, pady=10, sticky='e')

# Define the plot_accidents_by_date_and_type function


def plot_accidents_by_date_and_type(start_date, end_date, alcohol_related, accident_type):
    filtered_data = data[(data['ACCIDENT_DATE'] >= start_date)
                         & (data['ACCIDENT_DATE'] <= end_date)]

    if alcohol_related != "All":
        filtered_data = filtered_data[filtered_data['ALCOHOL_RELATED']
                                      == alcohol_related]

    if accident_type != "All":
        filtered_data = filtered_data[filtered_data['ACCIDENT_TYPE']
                                      == accident_type]

    accidents_by_date = filtered_data.groupby(
        'ACCIDENT_DATE').size().reset_index(name='Number_of_Accidents')

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(accidents_by_date['ACCIDENT_DATE'],
            accidents_by_date['Number_of_Accidents'], marker='o')
    ax.set(title='Number of Accidents by Date',
           xlabel='Date', ylabel='Number of Accidents')
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=second_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, padx=10, pady=10)
    canvas.draw()


# Run the Tkinter event loop
root.mainloop()
