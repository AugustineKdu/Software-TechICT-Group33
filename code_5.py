import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db_create import create_db
from first_graph import get_data_for_first_graph
from second_graph import get_data_for_second_graph
from third_graph import get_data_for_third_graph
from tkinter import PhotoImage

# create database if not exist
database_file = "Crash Statistics Victoria.db"
if os.path.exists(database_file):
    pass
else:
    create_db()

# Get the date range of database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()
cursor.execute("SELECT min(ACCIDENT_DATE), max(ACCIDENT_DATE) FROM Crash")
data = cursor.fetchone()
min_date = data[0]
max_date = data[-1]
conn.close()

# Create the main window
root = tk.Tk()
root.title("Accident Analysis")

# user Manual frame
user_manual_frame = tk.Frame(root, bg='#65C5AE')
user_manual_frame.pack(fill='x')

# graph search frame
graph_search_frame = tk.Frame(root, bg='#13093D')
graph_search_frame.pack(fill='x')

# outcome graph frame
graph_frame = tk.Frame(root, width=300, height=200)
graph_frame.pack(fill='x')

# table search frame
table_search_frame = tk.Frame(root, bg='#13093D')
table_search_frame.pack(fill='x')

# outcome table frame
table_frame = tk.Frame(root, width=300, height=50)
table_frame.pack(side=tk.TOP)
tree = ttk.Treeview(table_frame, columns=("OBJECTID", "ACCIDENT_NO", "ACCIDENT_DATE", "ACCIDENT_TIME", "ALCOHOL_RELATED",
                                          "ACCIDENT_TYPE", "SEVERITY", "REGION_NAME"), show="headings")


# Define the graph search frame components
title_label = tk.Label(
    graph_search_frame, text="Search For Data Charts", font=("Arial", 18, "bold"), bg='#13093D', fg='white')
title_label.grid(row=0, column=4, columnspan=4, padx=10, pady=10, sticky='w')

start_date_label = tk.Label(
    graph_search_frame, text="Start Date:", bg='#13093D', fg='white')
start_date_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

start_date_entry = tk.Entry(graph_search_frame)
start_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

end_date_label = tk.Label(
    graph_search_frame, text="End Date:", bg='#13093D', fg='white')
end_date_label.grid(row=1, column=2, padx=10, pady=10, sticky='w')

end_date_entry = tk.Entry(graph_search_frame)
end_date_entry.grid(row=1, column=3, padx=10, pady=10, sticky='w')

date_range_label = tk.Label(
    graph_search_frame, text=f"Selectable Date Range: {min_date} to {max_date}", font=('Arial', 12), bg='#13093D', fg='white')
date_range_label.grid(row=0, column=0, columnspan=4, pady=10, sticky='s')

alcohol_related_label = tk.Label(
    graph_search_frame, text="Alcohol Related:", bg='#13093D', fg='white')
alcohol_related_label.grid(row=1, column=4, padx=(10, 0), pady=10, sticky='e')
alcohol_related_options = ["All", "Yes", "No"]
alcohol_related_combobox = ttk.Combobox(
    graph_search_frame, values=alcohol_related_options, state="readonly")
alcohol_related_combobox.set("All")
alcohol_related_combobox.grid(
    row=1, column=5, padx=(0, 10), pady=10, sticky='w')

category_label = tk.Label(
    graph_search_frame, text="Category:", bg='#13093D', fg='white')
category_label.grid(row=1, column=6, padx=(10, 0), pady=10, sticky='e')
category_options = ["ACCIDENT_TYPE", "SEVERITY", "REGION_NAME"]
category_combobox = ttk.Combobox(
    graph_search_frame, values=category_options, state="readonly")
category_combobox.set("ACCIDENT_TYPE")
category_combobox.grid(row=1, column=7, padx=(0, 10), pady=10, sticky='w')


# # Add a logo
logo = tk.PhotoImage(file="StateImage3.png")
logo_label = tk.Label(user_manual_frame, image=logo,
                      borderwidth=0, highlightthickness=0)
logo_label.pack(side='left', padx=0)

# Add project name
project_name_label = tk.Label(
    user_manual_frame, text="Victoria State Accident Dashboard", font=('Arial', 44), bg='#65C5AE', fg='white')
project_name_label.pack(side='left', padx=5)

# User Manual in a Text Widget
user_manual = tk.Text(user_manual_frame, height=10,
                      width=120, bg='#65C5AE', fg='white', font=('Arial', 18))
user_manual.pack(padx=10, pady=10)
user_manual.insert(tk.END, "User Manual\n\n")
user_manual.insert(
    tk.END, "1. Choose the desired start and end dates for accident analysis.\n")
user_manual.insert(
    tk.END, "2. Choose whether to filter results by alcohol-related accidents.\n")
user_manual.insert(
    tk.END, "3. Choose the type of accident for further filtering if needed.\n")
user_manual.insert(
    tk.END, "4. Click the 'Search' button to display the graph based on your selections.\n")
user_manual.config(state=tk.DISABLED)  # Make the text read-only

# Define the graph search button


def graph_search():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    alcohol_related = alcohol_related_combobox.get()
    category = category_combobox.get()

    if start_date < min_date or end_date > max_date:
        messagebox.showerror(
            "Invalid Date", "Please enter a valid date in YYYY/MM/DD format.")
    else:
        display_graph(start_date, end_date, alcohol_related, category)


graph_search_button = tk.Button(
    graph_search_frame, text="Search", command=graph_search)
graph_search_button.grid(row=1, column=8, padx=10, pady=10, sticky='e')


# Function for display graph
def display_graph(start_date, end_date, alcohol_related, category):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 5))
    (y, x, count) = get_data_for_first_graph(start_date, end_date)
    ax1.plot(count, y, color="blue", linewidth=2.5, linestyle="-")
    ax1.set(title=f'Average Number of Accidents Per Hour from {start_date} to {end_date}',
            xlabel='Time (Hourly)', ylabel='Number of Accidents')
    ax1.set_xticks(count)
    ax1.set_xticklabels(x, fontsize=7, rotation=5)
    ax1.grid(False)

    (y, x, count) = get_data_for_second_graph(
        start_date, end_date, alcohol_related, category)
    ax2.bar(count, y, color="green", width=0.1)
    ax2.set(title=f'The Total Number of Accidents by {category} from {start_date} to {end_date}',
            xlabel=category, ylabel='Number of Accidents')
    ax2.set_xticks(count)
    ax2.set_xticklabels(x, fontsize=7, rotation=5)
    ax2.grid(False)

    (y, x, count, label) = get_data_for_third_graph(
        start_date, end_date, alcohol_related, category)
    if category == "ACCIDENT_TYPE":
        ax3.plot(count, y[0], color="green", linewidth=1,
                 linestyle="-", label=label[0])
        ax3.plot(count, y[1], color="blue", linewidth=1,
                 linestyle="-", label=label[1])
        ax3.plot(count, y[2], color="orange", linewidth=1,
                 linestyle="-", label=label[2])
        ax3.plot(count, y[3], color="red", linewidth=1,
                 linestyle="-", label=label[3])
        ax3.plot(count, y[4], color="purple", linewidth=1,
                 linestyle="-", label=label[4])
        ax3.plot(count, y[5], color="brown", linewidth=1,
                 linestyle="-", label=label[5])
        ax3.plot(count, y[6], color="pink", linewidth=1,
                 linestyle="-", label=label[6])
        ax3.plot(count, y[7], color="cyan", linewidth=1,
                 linestyle="-", label=label[7])
        ax3.plot(count, y[8], color="gray", linewidth=1,
                 linestyle="-", label=label[8])
    elif category == "SEVERITY":
        ax3.plot(count, y[0], color="green", linewidth=1,
                 linestyle="-", label=label[0])
        ax3.plot(count, y[1], color="blue", linewidth=1,
                 linestyle="-", label=label[1])
        ax3.plot(count, y[2], color="orange", linewidth=1,
                 linestyle="-", label=label[2])
        ax3.plot(count, y[3], color="red", linewidth=1,
                 linestyle="-", label=label[3])
    elif category == "REGION_NAME":
        ax3.plot(count, y[0], color="green", linewidth=1,
                 linestyle="-", label=label[0])
        ax3.plot(count, y[1], color="blue", linewidth=1,
                 linestyle="-", label=label[1])
        ax3.plot(count, y[2], color="orange", linewidth=1,
                 linestyle="-", label=label[2])
        ax3.plot(count, y[3], color="red", linewidth=1,
                 linestyle="-", label=label[3])
        ax3.plot(count, y[4], color="purple", linewidth=1,
                 linestyle="-", label=label[4])
        ax3.plot(count, y[5], color="brown", linewidth=1,
                 linestyle="-", label=label[5])
        ax3.plot(count, y[6], color="pink", linewidth=1,
                 linestyle="-", label=label[6])
        ax3.plot(count, y[7], color="cyan", linewidth=1,
                 linestyle="-", label=label[7])
    ax3.set(
        title=f'The Number of Accidents by Month from {start_date} to {end_date}', xlabel='Period', ylabel='Number of Accidents')
    ax3.set_xticks(count)
    ax3.set_xticklabels(x, fontsize=7, rotation=90)
    ax3.grid(False)
    ax3.legend(loc="center right", prop={'size': 5})

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, padx=10, pady=10)
    canvas.draw()


# Define table search frame
title_label = tk.Label(
    table_search_frame, text="Search For Date Table", font=("Arial", 18, "bold"), bg='#13093D', fg='white')
title_label.grid(row=0, column=4, columnspan=4, padx=10, pady=10, sticky='w')

table_start_date_label = tk.Label(
    table_search_frame, text="Start Date:", bg='#13093D', fg='white')
table_start_date_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
table_start_date_entry = tk.Entry(table_search_frame)
table_start_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

table_end_date_label = tk.Label(
    table_search_frame, text="End Date:", bg='#13093D', fg='white')
table_end_date_label.grid(row=1, column=2, padx=10, pady=10, sticky='w')
table_end_date_entry = tk.Entry(table_search_frame)
table_end_date_entry.grid(row=1, column=3, padx=10, pady=10, sticky='w')

keyword_label = tk.Label(
    table_search_frame, text="Type a keyword for accident type:", bg='#13093D', fg='white')
keyword_label.grid(row=1, column=4, padx=(10, 0), pady=10, sticky='e')
keyword_entry = tk.Entry(table_search_frame)
keyword_entry.grid(row=1, column=5, padx=10, pady=10, sticky='w')

date_range_label = tk.Label(
    table_search_frame, text=f"Selectable Date Range: {min_date} to {max_date}", font=('Arial', 12), bg='#13093D', fg='white')
date_range_label.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky='s')

# Define the table search button


def table_search():
    start_date = table_start_date_entry.get()
    end_date = table_end_date_entry.get()
    keyword = keyword_entry.get()

    if start_date < min_date or end_date > max_date:
        messagebox.showerror(
            "Invalid Date", "Please enter a valid date in YYYY/MM/DD format.")
    else:
        display_table(start_date, end_date, keyword)


table_search_button = tk.Button(
    table_search_frame, text="Search", command=table_search)
table_search_button.grid(row=1, column=6, padx=10, pady=10, sticky='e')

# function for display table (add the keyword search box)


def display_table(start_date, end_date, keyword):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    query = """
            SELECT OBJECTID, ACCIDENT_NO, ACCIDENT_DATE, ACCIDENT_TIME, ALCOHOL_RELATED, ACCIDENT_TYPE, SEVERITY, REGION_NAME 
            FROM Crash WHERE ACCIDENT_DATE BETWEEN ? AND ? AND ACCIDENT_TYPE LIKE ?;
            """
    cursor.execute(query, (start_date, end_date, f"%{keyword}%"))
    rows = cursor.fetchall()

    # Clear existing data in the table (if any)
    for row in tree.get_children():
        tree.delete(row)

    # Insert fetched data into the table
    for row in rows:
        tree.insert('', 'end', values=row)

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

    scrollbar = ttk.Scrollbar(
        table_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)


# Run the Tkinter event loop
root.mainloop()
