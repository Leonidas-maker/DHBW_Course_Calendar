# imports
from icalendar import Calendar, Event
import requests
import os
from datetime import datetime, timedelta
import time
import hashlib
import shutil

now = datetime.today()

timestamp_week = (datetime.timestamp(now) + timedelta(days=7))
print(type(timestamp_week))

print(type(timedelta(days= 7).__str__))