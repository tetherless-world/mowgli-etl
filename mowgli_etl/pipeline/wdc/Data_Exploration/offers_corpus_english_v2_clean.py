from os import listdir

from mowgli_etl.paths import DATA_DIR

JSONL_DIR_PATH = DATA_DIR / "wdc" / "extracted"

# Generate a list of all possible jsonl files
directory = [item for item in listdir(JSONL_DIR_PATH) if ".jsonl" in item]

# Present options for jsonl files
print(
    "Please choose which of the following files you'd like to clean [enter number on the left]:\n"
)
for i in range(0, len(directory)):
    print("\t{} - {}".format(i, directory[i]))

# Have user select which file to clean
choice = directory[int(input("\nChosen file number: "))]

# Copy each line in the file
lines = [line for line in open(JSONL_DIR_PATH / choice, "r")]

# Create cleaned file
with open(JSONL_DIR_PATH / (choice[0:-6] + "_clean.jsonl"), "w") as new_file:
    danger_string = '"brand":'
    for line in lines:
        # Catch lines with more than one object based on brand identifier
        if line.count(danger_string) == 1:
            new_file.write(line)
        else:
            # No brand case
            if line.count(danger_string) == 0:
                new_file.write(line)
            # Too many items
            if line.count(danger_string) > 1:
                # Track where the objects start
                data_starts = []
                val = 0
                while val != -1:
                    val = line.find(danger_string, val + 1)
                    # Make sure it's actually a new product
                    if line[val - 2] == ":" or val == -1:
                        continue
                    data_starts.append(val - 1)

                # Split into new lines in new file
                for i in range(len(data_starts)):
                    if i < len(data_starts) - 1:
                        new_file.write(line[data_starts[i] : data_starts[i + 1]] + "\n")
                    else:
                        print(line[data_starts[i] : :])
                        new_file.write(line[data_starts[i] : :])
                        # Weird bug. This works but a bit informal
