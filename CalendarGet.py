# imports
from icalendar import Calendar, Event
import requests
import os
from datetime import datetime, timedelta
import time as t
import hashlib
import shutil
import recurring_ical_events

# url to download ics file
url = "http://vorlesungsplan.dhbw-mannheim.de/ical.php?uid=8537001"

# save content in doc
doc = requests.get(url)

#saves old path
with open("tmp/past_path.txt", "r") as f:
    past_path = f.read()

# gets todays date and new format
now = datetime.now()
week = now + timedelta(days=7)

time = now.strftime("%H_%M_%S")

#creates time folder
try:
    os.mkdir("src/" + time)
    print("Directory " + time + " created")
except FileExistsError:
    print("Directory " + time + " already exists")

# creates file "DHBW_cal.ics" in folder src
open("src/" + time + "/DHBW_cal.ics", "wb").write(doc.content)

# hash file and creates "cal_hash.txt"
file = ("src/" + time + "/DHBW_cal.ics")
BLOCK_SIZE = 65536

file_hash = hashlib.sha256()
with open(file, "rb") as f:
    fb = f.read(BLOCK_SIZE)
    while len(fb) > 0:
        file_hash.update(fb)
        fb = f.read(BLOCK_SIZE)

hash = file_hash.hexdigest()

open("src/" + time + "/cal_hash.txt", "w").write(hash)

# creates file "timestamp"
timestamp = str(datetime.timestamp(now))

open("src/" + time + "/timestamp.txt", "w").write(timestamp)

# hardcoded hash compare for test (later better)
with open(past_path + "/cal_hash.txt", encoding = "utf-8") as f: 
    old_hash = f.read()

with open("src/" + time + "/cal_hash.txt", encoding = "utf-8") as f:
    new_hash = f.read()

if old_hash == new_hash:
    print("nichts zu tun")
if old_hash != new_hash:
    print("der Kalender hat sich geändert!")

timestamp_week = datetime.timestamp(now) + 604800

# get all events
cal_file = open("src/" + time + "/DHBW_cal.ics", "rb")
cal = Calendar.from_ical(cal_file.read())

cal_file.close()

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
            with open("src/" + time + "/calendar.ics", "wb") as f:
                event = Event()
                event["SUMMARY"] = summary
                event["dtstart"] = dtstart
                event["dtend"] = dtend
                event["LOCATION"] = location
                cal_new.add_component(event)
                f.write(cal_new.to_ical())

new_ics_file = open("src/" + time + "/calendar.ics", "rb")
old_ics_file = open(past_path + "/calendar.ics", "rb")

new_icsCalender = Calendar.from_ical(new_ics_file.read())
old_icsCalender = Calendar.from_ical(old_ics_file.read())

new_ics_file.close()
old_ics_file.close()

current = now.strftime("%Y%m%dT%H%M%SZ")
week_time = week.strftime("%Y%m%dT%H%M%SZ")

events = recurring_ical_events.of(new_icsCalender).between(current, week_time)

new_L = []
old_L = []
new_count = 0
old_count = 0

for event in events:
    summary = event["SUMMARY"]
    start = event["DTSTART"].dt
    duration = event["DTEND"].dt - event["DTSTART"].dt
    location = event["LOCATION"]
    new_L.append("{}; {}; {}; {}".format(start, duration, summary, location))
    new_count = new_count + 1

events = recurring_ical_events.of(old_icsCalender).between(current, week_time)

for event in events:
    summary = event["SUMMARY"]
    start = event["DTSTART"].dt
    duration = event["DTEND"].dt - event["DTSTART"].dt
    location = event["LOCATION"]
    old_L.append("{}; {}; {}; {}".format(start, duration, summary, location))
    old_count = old_count + 1

i = 0

while i < new_count:
    if old_L[i] != new_L[i]:
        change = new_L[i] + "\n"
        open("src/" + time + "/change.txt", "a").write(change)
    i = i + 1

shutil.rmtree(past_path)

print("Directory " + past_path + " removed")

open("tmp/past_path.txt", "w").write("src/" + time)