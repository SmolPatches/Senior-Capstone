import random
from faker import Faker
import csv
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

# make servers 
all_servers_data = []
fake_max = 150_000 # max_id not for faker to use
<<<<<<< HEAD
server_entry_num = 110_000 # now 
=======
server_entry_num = 150_000 # now 
VIRT_NUM = 5_000
PHYS_NUM = 1_000
>>>>>>> f4999a8 (added server counts)
# Generate data for all servers
server_ids = [f"SRV-{make_id(fake_max)}" for i in range(server_entry_num)]
# Define constants and lists for server dataset
OS_LIST = ["Linux", "Windows"]
DATA_CENTERS = [f"DC-{i:01}" for i in range(1, 11)]
PHYSICAL_SERVERS = [server_ids[i] for i in range(PHYS_NUM)] # 10k physical 
VIRTUAL_SERVERS = [server_ids[i] for i in range(VIRT_NUM)] # 100k virts 
# Generate data for all physical servers
for server in PHYSICAL_SERVERS:  
    server_name = server
    os_type = "VirtualBox"
    data_center = random.choice(DATA_CENTERS)
    is_virtual = "No"
    parent_server = "N/A"
    
    all_servers_data.append({
        "Name": server_name,
        "OS": os_type,
        "DataCenter": data_center,
        "IsVirtual": is_virtual,
        "ParentServer": parent_server
    })


# Generate data for all virtual servers
for server in VIRTUAL_SERVERS:
    server_name = server
    os_type = random.choice(OS_LIST)
    parent_server = random.choice(PHYSICAL_SERVERS)
    # Extracting the data center from the associated physical server
    data_center = next(item for item in all_servers_data if item.get("Name") == parent_server).get("DataCenter")
    is_virtual = "Yes"
    
    all_servers_data.append({
        "Name": server_name,
        "OS": os_type,
        "DataCenter": data_center,
        "IsVirtual": is_virtual,
        "ParentServer": parent_server
    })

# Specify the CSV file name
csv_file_name = 'Servers.csv'
server_txt_name = "servers.txt" # used for parity of servers in other files
# Write all server data to the CSV file
with open(csv_file_name, mode='w', newline='') as csv_file:
    fieldnames = ["Name", "OS", "DataCenter", "IsVirtual", "ParentServer"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write the data entries, including empty rows
    for entry in all_servers_data:
        writer.writerow(entry)
with open(server_txt_name,"w") as server_file:
    server_file.write(",".join(server_ids))
print(f"Generated CSV: {csv_file_name}\tServer List:{server_txt_name}")