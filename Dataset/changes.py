import random
import csv
from datetime import datetime, timedelta
from faker import Faker
fake = Faker("en_US")
# Define constants
NUM_RECORDS = 5_000 # 50k changes 
fake_max = 100_000 #max for id gen 
MAX_DAYS_DIFF = 2*365  # Max number of days between StartDate and EndDate
DESCRIPTIONS = ["Windows Patching", "Linux patching", "Database upgrade", "Firmware update", "Network reconfiguration"]
SERVERS = []
debug = False
def make_id(fake_max):
    rand_int = fake.unique.random_int(0,fake_max)
    rand_str = str(rand_int)
    fake_max_str = str(fake_max)
    len_diff = len(fake_max_str) - len(rand_str)
    if len_diff == 0:
        return rand_int
    if len_diff > 0 :
        return "0"*len_diff + rand_str
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
    end_date = start_date + timedelta(MAX_DAYS_DIFF)
    end_epoch_time = int(end_date.timestamp()) #in seconds
    description = random.choice(DESCRIPTIONS)
    # get random servers for affectedservers
    serv_tmp = []
    serv_count = random.randint(2,10)
    for _ in range(serv_count):
        serv_tmp.append(random.choice(SERVERS))
    # 
    serv_tmp = ": ".join(serv_tmp)

    data.append({
        "ID": f"CHG-{make_id(fake_max)}",
        "StartDate": start_date.strftime('%m/%d/%y %H:%M'),
        "StartEpochTime": start_epoch_time,
        "EndDate": end_date.strftime('%m/%d/%y %H:%M'),
        "EndEpochTime": end_epoch_time,
        "Description": description,
        "AffectedServer": serv_tmp 
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
