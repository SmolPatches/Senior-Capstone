import random
import csv
from datetime import datetime, timedelta
from faker import Faker
fake = Faker("en_US")
def make_id(fake_max):
    rand_int = fake.unique.random_int(0,fake_max)
    rand_str = str(rand_int)
    fake_max_str = str(fake_max)
    len_diff = len(fake_max_str) - len(rand_str)
    if len_diff == 0:
        return rand_int
    if len_diff > 0 :
        return "0"*len_diff + rand_str
# Number of data entries to generate
num_entries = int(1_000_000) # evaluation value
fake_max = int(2_000_000)
days = 2*365
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
    "CPU has exceeded threshold: (75%) currently ({0:.2f}%)",
    "Laptop LAQ{0} shuts down due to overheating",
    "Server SRV-{0} experienced a memory leak",
    "Application on SRV-{0} failed to start after update",
    "Server SRV-{0} ran out of memory and was rebooted",
    "Disk space on SRV-{0} is below 10% available",
    "SRV-{0} failed to establish a network connection",
    "Unexpected disk I/O spike detected on SRV-{0}",
    "Storage subsystem on SRV-{0} reported read/write errors",
    "Network interface on SRV-{0} dropped packets for 10 minutes"
]

# Function to generate a random date and time within the past month
def random_date():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    random_date = start_date + (end_date - start_date) * random.random()
    formatted_date = random_date.strftime('%m/%d/%y %H:%M')
    epoch_time = int(random_date.timestamp()) #in seconds
    return formatted_date, epoch_time

# Generate data entries
data_entries = []
for _ in range(num_entries):
    reported_date, epoch_time = random_date()
    entry = {
        "ID": f"INC-{make_id(fake_max)}",
        "Severity": random.choice(severities),
        "AffectedServer": random.choice(servers),
        "ReportedDate": reported_date,
        "EpochTime": epoch_time,
        "Description": random.choice(descriptions).format(random.randint(1, 9999999))
    }
    data_entries.append(entry)

# Specify the CSV file name
csv_file_name = 'Incidents.csv'

# Write data entries to the CSV file
with open(csv_file_name, mode='w', newline='') as csv_file:
    fieldnames = ["ID", "Severity", "AffectedServer", "ReportedDate", "EpochTime", "Description"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data entries
    for entry in data_entries:
        writer.writerow(entry)

print(f"Data has been written to {csv_file_name}")
