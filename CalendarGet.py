# imports
from icalendar import Calendar, Event
import requests
import os
from datetime import datetime, timedelta
import time
import hashlib
import shutil

# url to download ics file
url = "http://vorlesungsplan.dhbw-mannheim.de/ical.php?uid=8537001"

# save content in doc
doc = requests.get(url)

# gets todays date and new format
now = datetime.now()

day = now.strftime("%d_%m_%Y")
print(day)

time = now.strftime("%H_%M_%S")
print(time)

#creates day folder
try:
    os.mkdir("src/" + day)
    print("Directory " + day + " Created")
except FileExistsError:
    print("Directory " + day + " already exists")

#creates time folder
try:
    os.mkdir("src/" + day + "/" + time)
    print("Directory " + time + " Created")
except FileExistsError:
    print("Directory " + time + " already exists")

# creates file "DHBW_cal.ics" in folder src
open("src/" + day + "/" + time + "/DHBW_cal.ics", "wb").write(doc.content)

# hash file and creates "cal_hash.txt"
file = ("src/" + day + "/" + time + "/DHBW_cal.ics")
BLOCK_SIZE = 65536

file_hash = hashlib.sha256()
with open(file, "rb") as f:
    fb = f.read(BLOCK_SIZE)
    while len(fb) > 0:
        file_hash.update(fb)
        fb = f.read(BLOCK_SIZE)

hash = file_hash.hexdigest()
print(hash) # for debugging

open("src/" + day + "/" + time + "/cal_hash.txt", "w").write(hash)

# creates file "timestamp"
timestamp = str(datetime.timestamp(now))

open("src/" + day + "/" + time + "/timestamp.txt", "w").write(timestamp)

# hardcoded hash compare for test (later better)
with open("other_data/cal_hash.txt", encoding = "utf-8") as f:
    hash1 = f.read()

with open("src/" + day + "/" + time + "/cal_hash.txt", encoding = "utf-8") as f:
    hash2 = f.read()

print(hash1) # for debugging
print(hash2) # for debugging

if hash1 == hash2:
    print("nichts zu tun")
if hash1 != hash2:
    print("der Kalender hat sich geändert!")

timestamp_week = datetime.timestamp(now) + 604800

# get all events
cal_file = open("src/" + day + "/" + time + "/DHBW_cal.ics", "rb")
cal = Calendar.from_ical(cal_file.read())

cal_new = Calendar()

for component in cal.subcomponents:
    if component.name == "VEVENT":
        summary = component.get("summary")
        dtstart = component.get("dtstart")
        dtend = component.get("dtend")
        location = component.get("location")

        if location == "":
            location = "Online"

        # compares time and save only events in future
        if float(timestamp) <= datetime.timestamp(component.get("dtstart").dt) < timestamp_week: 
            with open("src/" + day + "/" + time + "/calendar.ics", "wb") as f:
                event = Event()
                event["SUMMARY"] = summary
                event["dtstart"] = dtstart
                event["dtend"] = dtend
                event["LOCATION"] = location
                cal_new.add_component(event)
                f.write(cal_new.to_ical())

#path = "src/24_11_2022/16_31_03"
#shutil.rmtree(path)