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

# Test
races = read_lif_file('045-Champ Final-01.lif')

print(f"Total races found: {len(races)}\n")
for i, race in enumerate(races):
    print(f"--- Race {i + 1} ---")
    for line in race:
        print(line)
    print()
