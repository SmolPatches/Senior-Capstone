#DataCenter

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

# Return the generated data centers for verification
data_centers
