import random
import csv
from datetime import datetime, timedelta
from faker import Faker
fake = Faker("en_US")
# Number of data entries to generate
num_entries = int(1e4) # sane default
debug = False
# Lists for random selection
severities = ["1-High", "2-Medium", "3-Low", "4-Very Low"]
servers = []
server_txt_name = "servers.txt" # used for parity of servers in other files
try:
    with open(server_txt_name,"r") as server_ids:
        servers = server_ids.read().split(",")
        if debug == True:
            print(f"servers: {servers}")
except FileNotFoundError as e:
    print(e)
    print("You must run servers.py first in order to generate a servers.txt file")
    raise SystemExit
descriptions = [
    "CPU has exceeded threshold: (75%) currently ({:.2f}%)",
    "Server SRV-{0} experienced a memory leak",
    "Application on SRV-{0} failed to start after update"
]

# Function to generate a random date and time within the past month
def random_date():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime('%m/%d/%y %H:%M')

# Generate data entries
data_entries = []
for _ in range(num_entries):
    entry = {
        "ID": f"INC-{fake.random_int(1000001, 1999999)}",
        "Severity": random.choice(severities),
        "AffectedServer": random.choice(servers),
        "ReportedDate": random_date(),
        "Description": random.choice(descriptions).format(random.randint(1, 9999999))
    }
    data_entries.append(entry)

# Specify the CSV file name
csv_file_name = 'Incidents.csv'

# Write data entries to the CSV file
with open(csv_file_name, mode='w', newline='') as csv_file:
    fieldnames = ["ID", "Severity", "AffectedServer", "ReportedDate", "Description"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data entries
    for entry in data_entries:
        writer.writerow(entry)

print(f"Data has been written to {csv_file_name}")
