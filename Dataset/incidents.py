import random
from datetime import datetime, timedelta

# Number of data entries to generate
num_entries = 100

# Lists for random selection
severities = ["1-High", "2-Medium", "3-Low", "4-Very Low"]
servers = [f"SRV-{str(i).zfill(7)}" for i in range(1, 11)]  # Generate 10 server names for demo purposes
descriptions = [
    "CPU has exceeded threshold: (75%) currently ({:.2f}%)",
    "Laptop LAQ{0} shuts down due to overheating",
    "Server SRV-{0} experienced a memory leak",
    "Application on SRV-{0} failed to start after update"
]

# Function to generate a random date and time within the past month
def random_date():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime('%m/%d/%y %H:%M')

# Generate data entries
data_entries = []
for _ in range(num_entries):
    entry = {
        "ID": f"INC-{random.randint(1000001, 1999999)}",
        "Severity": random.choice(severities),
        "AffectedServer": random.choice(servers),
        "ReportedDate": random_date(),
        "Description": random.choice(descriptions).format(random.randint(1, 9999999))
    }
    data_entries.append(entry)

data_entries[:5]  # Display the first 5 entries for review
