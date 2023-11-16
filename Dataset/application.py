#Application
from faker import Faker
from os import urandom
from pprint import pprint
import random
import csv
faker = Faker("en_US")
seed = urandom(64)
Faker.seed(seed)
fake_max =2e4 # random_int to be used
use_faker = True
def make_app_id(fake_max,rand_int):
    rand_str = str(rand_int)
    fake_max_str = str(fake_max)
    len_diff = len(fake_max_str) - len(rand_str)
    if len_diff == 0:
        return rand_int
    if len_diff > 0 :
        return "0"*len_diff + rand_str

# utilize faker.company()

# Define constants and lists
APP_NAMES = [
    "Mango Tango App", "Cool Cats App", "Jazzy Java App", "Stellar Spaces App",
    "Neptune Notes App", "Moonwalk Music App", "Sunny Safari App", "Pixel Pals App",
    "Doodle Dots App", "Terra Tracks App"
]
ALL_SERVERS = [f"SRV-010{i:01}" for i in range(1, 10000)] + [f"SRV-100{i:01}" for i in range(1, 10000)]

# Generate the dataset for APP-1001 through APP-1999
applications_data = []
for i in range(1, 2000):  # From APP-1001 to APP-1999
    # use company based name for each app if use_faker is true
    app_name = f'APP-{make_app_id(fake_max,faker.random_int(0,fake_max))}' if use_faker else f"APP-{1000 + i}"
    # use company based description if faker is enabled
    description = faker.bs() if use_faker else random.choice(APP_NAMES)
    num_servers = random.randint(1, 10)
    servers = ", ".join(random.sample(ALL_SERVERS, num_servers))

    applications_data.append({
        "Name": app_name,
        "Description": description,
        "Servers": servers
    })

# Specify the CSV file name
csv_file_name = 'applications_data.csv'

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