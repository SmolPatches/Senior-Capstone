import random
import csv

# Define constants and lists for server dataset
OS_LIST = ["Linux", "Windows"]
DATA_CENTERS = [f"DC-{i:01}" for i in range(1, 11)]
PHYSICAL_SERVERS = [f"SRV-010{str(i).zfill(3)}" for i in range(1, 10000)]

# Generate data for all servers
all_servers_data = []

# Generate data for all physical servers
for i in range(1, 10000):  # From SRV-010001 to SRV-019999
    server_name = f"SRV-010{i:03}"
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

# Add empty rows (you can specify how many you want)
empty_rows = 10
for _ in range(empty_rows):
    all_servers_data.append({})

# Generate data for all virtual servers
for i in range(1, 10000):  # From SRV-100001 to SRV-199999
    server_name = f"SRV-100{i:03}"
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
csv_file_name = 'servers_data.csv'

# Write all server data to the CSV file
with open(csv_file_name, mode='w', newline='') as csv_file:
    fieldnames = ["Name", "OS", "DataCenter", "IsVirtual", "ParentServer"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write the data entries, including empty rows
    for entry in all_servers_data:
        writer.writerow(entry)

print(f"Server data has been written to {csv_file_name}")
