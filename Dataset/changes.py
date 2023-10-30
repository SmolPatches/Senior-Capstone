import random
import csv
from datetime import datetime, timedelta

# Define constants
NUM_RECORDS = 19999  # From CHG-10001 to CHG-19999
MAX_DAYS_DIFF = 7  # Max number of days between StartDate and EndDate
SERVER_ID_RANGE = 1000  # Server IDs from SRV-0000001 to SRV-0010000
DESCRIPTIONS = ["Windows Patching", "Linux patching", "Database upgrade", "Firmware update", "Network reconfiguration"]

# Method to generate a random date within the last two years
def random_date():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2*365)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date

# Method to generate a random list of servers
def random_servers():
    num_servers = random.randint(1, SERVER_ID_RANGE)
    servers = random.sample(range(1, SERVER_ID_RANGE + 1), num_servers)
    return [f"SRV-{server:07}" for server in servers]

# Generate the dataset
data = []

for _ in range(NUM_RECORDS):
    start_date = random_date()
    end_date = start_date + timedelta(days=random.randint(1, MAX_DAYS_DIFF))
    description = random.choice(DESCRIPTIONS)
    servers = ": ".join(random_servers())

    data.append({
        "ID": f"CHG-{10001 + _}",
        "StartDate": start_date.strftime('%m/%d/%y %H:%M'),
        "EndDate": end_date.strftime('%m/%d/%y %H:%M'),
        "Description": description,
        "AffectedServer": servers
    })

# Specify the CSV file name
csv_file_name = 'Changes.csv'

# Write data to the CSV file
with open(csv_file_name, mode='w', newline='') as csv_file:
    fieldnames = ["ID", "StartDate", "EndDate", "Description", "AffectedServer"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write the data entries
    for entry in data:
        writer.writerow(entry)

print(f"Data has been written to {csv_file_name}")
