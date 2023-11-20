import random
import csv
from datetime import datetime, timedelta

# Define constants
NUM_RECORDS = 19999  # From CHG-10001 to CHG-19999
MAX_DAYS_DIFF = 7  # Max number of days between StartDate and EndDate
SERVER_ID_RANGE = 1000  # Server IDs from SRV-0000001 to SRV-0010000
DESCRIPTIONS = ["Windows Patching", "Linux patching", "Database upgrade", "Firmware update", "Network reconfiguration"]
SERVERS = []
debug = False
# Method to generate a random date within the last two years
def random_date():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2*365)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date

server_txt_name = "servers.txt" # used for parity of servers in other files
try:
    with open(server_txt_name,"r") as server_ids:
        SERVERS = server_ids.read().split(",")
        if debug == True:
            print(f"servers: {SERVERS}")
except FileNotFoundError as e:
    print(e)
    print("You must run servers.py first in order to generate a servers.txt file")
    raise SystemExit
# Generate the dataset
data = []

for _ in range(NUM_RECORDS):
    start_date = random_date()
    start_epoch_time = int(start_date.timestamp()) #in seconds
    end_date = start_date + timedelta(days=random.randint(1, MAX_DAYS_DIFF))
    end_epoch_time = int(end_date.timestamp()) #in seconds
    description = random.choice(DESCRIPTIONS)
    servers = ": ".join(SERVERS)

    data.append({
        "ID": f"CHG-{10001 + _}",
        "StartDate": start_date.strftime('%m/%d/%y %H:%M'),
        "StartEpochTime": start_epoch_time,
        "EndDate": end_date.strftime('%m/%d/%y %H:%M'),
        "EndEpochTime": end_epoch_time,
        "Description": description,
        "AffectedServer": servers
    })

# Specify the CSV file name
csv_file_name = 'Changes.csv'

# Write data to the CSV file
with open(csv_file_name, mode='w', newline='') as csv_file:
    fieldnames = ["ID", "StartDate", "StartEpochTime", "EndDate", "EndEpochTime", "Description", "AffectedServer"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write the data entries
    for entry in data:
        writer.writerow(entry)

print(f"Data has been written to {csv_file_name}")
