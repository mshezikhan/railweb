# -*- coding: utf-8 -*-

import csv

# Read dataset.csv and extract unique station name ? code map
stations = {}

with open("dataset.csv", encoding="utf-8") as f:
    reader = csv.reader(f, quotechar="'", skipinitialspace=True)
    header = next(reader)

    # headers (from your example):
    # ["Train No.", "train Name", "islno", "station Code", "Station Name",
    #  "Arrival time", "Departure time", "Distance", "Source Station Code", "source Station Name",
    #  "Destination station Code", "Destination Station Name"]

    for row in reader:
        # Trim station code and name (remove extra spaces)
        station_code = row[3].strip()              # "station Code"
        station_name = row[4].strip()              # "Station Name"

        # Also grab source and destination while we’re here (optional but safe)
        src_code = row[8].strip()                  # "Source Station Code"
        src_name = row[9].strip()                  # "source Station Name"
        dst_code = row[10].strip()                 # "Destination station Code"
        dst_name = row[11].strip()                 # "Destination Station Name"

        # Add to map
        if station_code:
            stations[station_name] = station_code
        if src_code:
            stations[src_name] = src_code
        if dst_code:
            stations[dst_name] = dst_code

# Write stations.js in frontend/public/ or wherever your JS lives
JS_PATH = "../frontend/stations.js"  # adjust to your project

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write("// Auto?generated from dataset.csv\n")
    f.write("const stationMap = {\n")

    items = sorted(stations.items())
    for i, (name, code) in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        f.write(f'    "{name}": "{code}"{comma}\n')

    f.write("};\n")

print(f"Wrote {len(stations)} stations to {JS_PATH}")
