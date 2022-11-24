# imports
from ics import Calendar
import requests
import os
from datetime import datetime
import time
import hashlib

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