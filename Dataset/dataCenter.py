import random
import csv

state_city_mapping = {
    "TX": ["Houston", "Dallas", "Austin", "San Antonio"],
    "VA": ["Richmond", "Norfolk", "Arlington", "Alexandria"],
    "CA": ["Los Angeles", "San Francisco", "San Diego", "Sacramento"],
    "NY": ["New York", "Buffalo", "Rochester", "Albany"]
}

# Generate the dataset for data centers
data_centers = []

for i in range(1, 11):  # From DC-01 to DC-10
    state = random.choice(list(state_city_mapping.keys()))
    city = random.choice(state_city_mapping[state])

    data_centers.append({
        "Name": f"DC-{i:01}",
        "State": state,
        "City": city
    })

# Specify the CSV file name
csv_file_name = 'DataCenters.csv'

# Write data centers to the CSV file
with open(csv_file_name, mode='w', newline='') as csv_file:
    fieldnames = ["Name", "State", "City"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write the data centers
    for center in data_centers:
        writer.writerow(center)

print(f"Data centers have been written to {csv_file_name}")
