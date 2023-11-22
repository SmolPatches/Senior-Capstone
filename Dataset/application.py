#Application
from faker import Faker
from os import urandom
from pprint import pprint
import random
import csv
faker = Faker("en_US")
seed = urandom(64)
Faker.seed(seed)
APP_SIZE = 1_000
fake_max = 10_000 # random_int to be used
use_faker = True
def make_app_id(fake_max,rand_int):
    rand_str = str(rand_int)
    fake_max_str = str(fake_max)
    len_diff = len(fake_max_str) - len(rand_str)
    if len_diff == 0:
        return rand_int
    if len_diff > 0 :
        return "0"*len_diff + rand_str

# Define constants and lists
APP_NAMES = [
    "Mango Tango App", "Cool Cats App", "Jazzy Java App", "Stellar Spaces App",
    "Neptune Notes App", "Moonwalk Music App", "Sunny Safari App", "Pixel Pals App",
    "Doodle Dots App", "Terra Tracks App"
]
# servers parity amongst all files
ALL_SERVERS = []
server_txt_name = "servers.txt" # used for parity of servers in other files
try:
    with open(server_txt_name,"r") as server_ids:
        ALL_SERVERS = server_ids.read().split(",")
        print(f"servers: {ALL_SERVERS}")
except FileNotFoundError as e:
    print(e)
    print("You must run servers.py first in order to generate a servers.txt file")
    raise SystemExit
# Generate the dataset for APP-1001 through APP-1999
applications_data = []
for i in range(APP_SIZE):  # make 5000 random apps  
    # use company based name for each app if use_faker is true
    app_name = f'APP-{make_app_id(fake_max,faker.unique.random_int(0,fake_max))}' 
    # use company based description if faker is enabled
    description = faker.bs() if use_faker else random.choice(APP_NAMES)
    num_servers = random.randint(1, 10)
    servers = ": ".join(random.sample(ALL_SERVERS, num_servers))

    applications_data.append({
        "Name": app_name,
        "Description": description,
        "Servers": servers
    })

# Specify the CSV file name
csv_file_name = 'Applications.csv'

# Write application data to the CSV file
with open(csv_file_name, mode='w', newline='') as csv_file:
    fieldnames = ["Name", "Description", "Servers"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write the data entries
    for entry in applications_data:
        writer.writerow(entry)

print(f"Application data has been written to {csv_file_name}")
