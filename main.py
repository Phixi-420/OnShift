import pandas as pd
import tkinter as tk
from tkinter import ttk

# Initialize the schedule DataFrame
def load_schedule():
    columns = ['Employee Name', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    return pd.DataFrame(columns=columns)

# Function to add an employee to the schedule
def add_employee():
    employee_name = entry_employee_name.get()
    shift_details = [
        entry_sat.get(), entry_sun.get(), entry_mon.get(),
        entry_tue.get(), entry_wed.get(), entry_thu.get(), entry_fri.get()
    ]
    schedule_df.loc[len(schedule_df)] = [employee_name] + shift_details
    update_table()

# Function to remove an employee from the schedule
def remove_employee():
    employee_name = entry_employee_name.get()
    global schedule_df
    schedule_df = schedule_df[schedule_df['Employee Name'] != employee_name]
    update_table()

# Function to adjust a shift time for a specific employee and day
def adjust_shift(employee_name, day, shift_time):
    schedule_df.loc[schedule_df['Employee Name'] == employee_name, day] = shift_time

# Function to count the number of populated cells in each column (excluding headers)
def count_populated_cells():
    counts = {}
    for day in schedule_df.columns[1:]:  # Skip 'Employee Name'
        counts[day] = schedule_df[day].count()
    label_counts.config(text=f"Populated cells per day: {counts}")

# Function to update the displayed table in the GUI
def update_table():
    for row in tree.get_children():
        tree.delete(row)
    
    for index, row in schedule_df.iterrows():
        values = [row[col] for col in schedule_df.columns]
        tree.insert("", "end", values=values)

# Function to display the table with color-coding for "OFF" days
def display_schedule():
    for row in tree.get_children():
        tree.delete(row)
    
    for index, row in schedule_df.iterrows():
        values = [row[col] for col in schedule_df.columns]
        item = tree.insert("", "end", values=values)
        # Color code "OFF" days
        for i, val in enumerate(values[1:], start=1):
            if val == "OFF":
                tree.tag_configure("off", background="black", foreground="white")
                tree.item(item, tags="off")

# Set up the main tkinter window
root = tk.Tk()
root.title("Weekly Work Schedule")

# Schedule DataFrame
schedule_df = load_schedule()

# Entry widgets for employee details
frame_inputs = tk.Frame(root)
frame_inputs.pack()

tk.Label(frame_inputs, text="Employee Name").grid(row=0, column=0)
entry_employee_name = tk.Entry(frame_inputs)
entry_employee_name.grid(row=0, column=1)

# Day-specific entry fields
days = ['Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri']
entries = []
for i, day in enumerate(days):
    tk.Label(frame_inputs, text=day).grid(row=1, column=i)
    entry = tk.Entry(frame_inputs, width=5)
    entry.grid(row=2, column=i)
    entries.append(entry)

entry_sat, entry_sun, entry_mon, entry_tue, entry_wed, entry_thu, entry_fri = entries

# Button to add an employee
btn_add = tk.Button(frame_inputs, text="Add Employee", command=add_employee)
btn_add.grid(row=3, column=0, columnspan=2, pady=5)

# Button to remove an employee
btn_remove = tk.Button(frame_inputs, text="Remove Employee", command=remove_employee)
btn_remove.grid(row=3, column=2, columnspan=2, pady=5)

# Display table with Treeview widget
frame_table = tk.Frame(root)
frame_table.pack(pady=10)

columns = ['Employee Name', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri']
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=80)

tree.pack()

# Label to show populated cell counts
label_counts = tk.Label(root, text="Populated cells per day: ")
label_counts.pack()

# Button to count populated cells
btn_count = tk.Button(root, text="Count Populated Cells", command=count_populated_cells)
btn_count.pack(pady=5)

# Update table initially
update_table()

# Run the tkinter main loop
root.mainloop()

