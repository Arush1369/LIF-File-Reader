import os
import csv
from collections import defaultdict

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

    if not races:
        print("Warning: No races found in this file.")

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

def save_results_to_csv(scores, output_file='results.csv'):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Club Name', 'Points'])

        for club, points in sorted_scores:
            writer.writerow([club, points])

    print(f"Results saved to {output_file}")


folder_path = "X:\\OneDrive - Papatoetoe High School\\VS Code\\Sprint 3\\WakaNats2017"
club_scores = defaultdict(int)

for filename in os.listdir(folder_path):
    if filename.endswith('.lif'):
        filepath = os.path.join(folder_path, filename)
        print(f"Processing file: {filepath}")
        races = read_lif_file(filepath)
        assign_points(races, club_scores)

save_results_to_csv(club_scores)
