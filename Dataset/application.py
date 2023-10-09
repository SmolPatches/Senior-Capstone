#Application
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
    app_name = f"APP-{1000 + i}"
    description = random.choice(APP_NAMES)
    num_servers = random.randint(1, 10)
    servers = ", ".join(random.sample(ALL_SERVERS, num_servers))

    applications_data.append({
        "Name": app_name,
        "Description": description,
        "Servers": servers
    })

# Return first 5 rows to verify
applications_data[:5]
