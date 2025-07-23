import os
import csv
from tkinter import Tk, Label, Button, StringVar, Frame, filedialog, messagebox, Listbox

from collections import defaultdict

# === Data Processing Functions ===

def read_lif_file(filepath):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return []

    races = []
    current_race = []

    for line in lines:
        line = line.strip()

        if "Final" in line:
            if current_race:
                races.append(current_race)
            current_race = [line]
        else:
            if current_race:
                current_race.append(line)

    if current_race:
        races.append(current_race)

    return races

def assign_points(races, club_scores):
    points_table = [10, 7, 5, 3, 1]

    for race in races:
        for i, line in enumerate(race[1:6]):
            parts = line.split(",")
            if len(parts) > 5:
                club_name = parts[5].strip()
                if club_name:
                    points = points_table[i]
                    club_scores[club_name] += points

def save_results_to_csv(scores, output_file):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Club Name', 'Points'])

        for club, points in sorted_scores:
            writer.writerow([club, points])

# === GUI Logic ===

def select_source_folder():
    path = filedialog.askdirectory(title="Select Folder with .lif Files")
    if path:
        source_var.set(path)
        preview_data(path)  

def select_destination_file():
    file_path = filedialog.asksaveasfilename(
        title="Select destination file location and name",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )
    if file_path:
        destination_var.set(file_path)

def preview_data(source):
    club_scores = defaultdict(int)

    for filename in os.listdir(source):
        if filename.endswith('.lif'):
            filepath = os.path.join(source, filename)
            races = read_lif_file(filepath)
            assign_points(races, club_scores)

    sorted_scores = sorted(club_scores.items(), key=lambda x: x[1], reverse=True)

    listbox.delete(0, 'end')

    
    for club, points in sorted_scores:
        listbox.insert('end', f"{points:<5} points  {club}")

def run_processing():
    source = source_var.get()
    destination = destination_var.get()

    if not source:
        messagebox.showerror("Missing Info", "Please select a source folder.")
        return
    if not destination:
        messagebox.showerror("Missing Info", "Please select destination file location and name.")
        return

    club_scores = defaultdict(int)

    for filename in os.listdir(source):
        if filename.endswith('.lif'):
            filepath = os.path.join(source, filename)
            races = read_lif_file(filepath)
            assign_points(races, club_scores)

    save_results_to_csv(club_scores, destination)

    # Ask the user if they want to open the folder containing the saved CSV file
    open_folder_response = messagebox.askyesno(
        "Open Folder", 
        f"CSV file saved to:\n{destination}\n\nDo you want to open the folder?"
    )

    if open_folder_response:
        open_folder(destination)

def open_folder(path):
    
    folder_path = os.path.dirname(path)
    try:
        os.startfile(folder_path)  
    except Exception as e:
        print(f"Error opening folder: {e}")
        messagebox.showerror("Error", f"Unable to open folder: {e}")

# === GUI Setup ===

root = Tk()
root.title("LIF Race Points Processor")
root.geometry("700x400")
root.resizable(False, False)

# Variables
source_var = StringVar()
destination_var = StringVar()

# Header
Label(root, text="LIF Race Points Processor", font=("Arial", 16, "bold")).pack(pady=10)

# Source folder row
frame_source = Frame(root)
frame_source.pack(pady=5, fill='x', padx=20)
Button(frame_source, text="Select Source Folder", command=select_source_folder, width=35).pack(side='left')
Label(frame_source, textvariable=source_var, font=("Arial", 11), anchor='w', wraplength=400).pack(side='left', padx=10)

# Preview Listbox 
listbox = Listbox(root, width=60, height=10)
listbox.pack(pady=10)

# Destination file row 
frame_dest = Frame(root)
frame_dest.pack(pady=5, fill='x', padx=20)
Button(frame_dest, text="Select Destination File Location and Name", command=select_destination_file, width=35).pack(side='left')
Label(frame_dest, textvariable=destination_var, font=("Arial", 11), anchor='w', wraplength=400).pack(side='left', padx=10)

# Execute button
Button(root, text="Execute", command=run_processing, bg="#4CAF50", fg="white", font=("Arial", 12), width=20).pack(pady=20)

root.mainloop()
