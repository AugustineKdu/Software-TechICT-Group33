import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_data():
    file_path = filedialog.askopenfilename(title="Crash Statistics Victoria", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    
    global data
    data = pd.read_csv(file_path, parse_dates=['ACCIDENT_DATE'], dayfirst=True)
    accident_types = data['ACCIDENT_TYPE'].unique()

    # Populate the accident type comboboxes with unique accident types
    for combobox in accident_type_comboboxes:
        combobox["values"] = accident_types
        combobox.set("Select accident type")

def plot_accidents_by_date_and_type(start_date, end_date, selected_types):
    filtered_data = data[(data['ACCIDENT_DATE'] >= start_date) & (data['ACCIDENT_DATE'] <= end_date) & (data['ACCIDENT_TYPE'].isin(selected_types))]
    accidents_by_date = filtered_data.groupby('ACCIDENT_DATE').size().reset_index(name='Number_of_Accidents')
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(accidents_by_date['ACCIDENT_DATE'], accidents_by_date['Number_of_Accidents'], marker='o')
    ax.set(title='Number of Accidents by Date', xlabel='Date', ylabel='Number of Accidents')
    ax.grid(True)
    
    canvas = FigureCanvasTkAgg(fig, master=second_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, padx=10, pady=10)
    canvas.draw()

def search_by_date_and_type():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    selected_types = [combobox.get() for combobox in accident_type_comboboxes if combobox.get() != "Select accident type"]
    
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
        for widget in second_frame.winfo_children():
            widget.destroy()
        plot_accidents_by_date_and_type(start_date, end_date, selected_types)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid date format (YYYY-MM-DD).")

root = tk.Tk()
root.title("Crash Statistics in Victoria")
root.geometry("900x600")

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Load Data...", command=load_data)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

second_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=second_frame, anchor="nw")

search_panel = ttk.LabelFrame(second_frame, text="Search Panel", padding=(10, 5))
search_panel.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

start_date_label = ttk.Label(search_panel, text="Start Date (YYYY-MM-DD):")
start_date_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
start_date_entry = ttk.Entry(search_panel)
start_date_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

end_date_label = ttk.Label(search_panel, text="End Date (YYYY-MM-DD):")
end_date_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
end_date_entry = ttk.Entry(search_panel)
end_date_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

accident_type_comboboxes = []
for i in range(3):  # Allowing up to 3 accident types to be selected
    combobox = ttk.Combobox(search_panel, values=[], width=25)
    combobox.set("Select accident type")
    combobox.grid(row=i, column=2, sticky="ew", padx=5, pady=5)
    accident_type_comboboxes.append(combobox)

search_button = ttk.Button(search_panel, text="Search", command=search_by_date_and_type)
search_button.grid(row=3, columnspan=3, pady=5)

root.mainloop()
