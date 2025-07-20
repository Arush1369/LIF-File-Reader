def read_lif_file(filepath):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return

    print(f"Total lines: {len(lines)}")
    for line in lines[:5]:
        print(line.strip())

read_lif_file('002-Heat 1-02.lif')
