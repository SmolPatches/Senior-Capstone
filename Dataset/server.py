# Define constants and lists for server dataset
OS_LIST = ["Linux", "Windows"]
DATA_CENTERS = [f"DC-{i:01}" for i in range(1, 11)]
PHYSICAL_SERVERS = [f"SRV-010{str(i).zfill(3)}" for i in range(1, 10000)]

# Generate data for all physical servers
physical_servers_data = []

for i in range(1, 10000):  # From SRV-010001 to SRV-019999
    server_name = f"SRV-010{i:03}"
    os_type = "VirtualBox"
    data_center = random.choice(DATA_CENTERS)
    is_virtual = "No"
    parent_server = "N/A"
    
    physical_servers_data.append({
        "Name": server_name,
        "OS": os_type,
        "DataCenter": data_center,
        "IsVirtual": is_virtual,
        "ParentServer": parent_server
    })

# Generate data for all virtual servers
virtual_servers_data = []

for i in range(1, 10000):  # From SRV-100001 to SRV-199999
    server_name = f"SRV-100{i:03}"
    os_type = random.choice(OS_LIST)
    parent_server = random.choice(PHYSICAL_SERVERS)
    # Extracting the data center from the associated physical server
    data_center = next(item for item in physical_servers_data if item["Name"] == parent_server)["DataCenter"]
    is_virtual = "Yes"
    
    virtual_servers_data.append({
        "Name": server_name,
        "OS": os_type,
        "DataCenter": data_center,
        "IsVirtual": is_virtual,
        "ParentServer": parent_server
    })



# Return first 5 rows of each dataset to verify
physical_servers_data[4:9], virtual_servers_data[4:9]
