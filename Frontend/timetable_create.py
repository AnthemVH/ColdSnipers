import json
from datetime import datetime
import numpy as np

# Load your existing JSON file
with open("Frontend/stable_class_schedule_dataset.json", "r") as f:
    data = json.load(f)

# Populate parallel arrays
dates = data["dates"]
days = data["days"]

# Initialize times and classes arrays
times = []
classes = []

for date_entry in data["schedule"]:
    _, daily_times, daily_classes = date_entry
    print(daily_times)
    times.append(daily_times)
    classes.append(daily_classes)

def getindex_date(input):
    if input == "today":
        pass
    elif input == "tommrow":
        pass

def getindex_time(input):
    if input == "early":
        pass
    elif input == "latest":
        pass
    elif input == "next":
        pass
    