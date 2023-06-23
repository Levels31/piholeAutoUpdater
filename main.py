#! /usr/bin/env python3

from datetime import datetime, timedelta
import logging
import subprocess
from utils import sendmail

old = None
new = None
component = None
body = str()
update_available = False

# get current time
today_date = datetime.now().strftime("%d.%m.%Y")
today_date = datetime.strptime(today_date, "%d.%m.%Y")

# read log into memory
with open ("run.log", "r") as log:
    lines = log.readlines()

# Filter out lines with old timestamps
new_lines = []
for line in lines:
    timestamp_str, rest_of_line = line.split(" ", 1)
    timestamp_str = datetime.strptime(timestamp_str, "%d.%m.%Y")
    
    if today_date - timedelta(days=30) < timestamp_str:
        new_lines.append(line)

# write modified content back to file
with open("run.log", "w") as file:
    file.writelines(new_lines)   

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d.%m.%Y %H:%M:%S Uhr: ', filename='run.log', encoding='utf-8', level=logging.DEBUG)
date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

logging.info("**********************")
logging.info("Reading pihole version")
stream = subprocess.run(['pihole', '-v'], stdout=subprocess.PIPE)

output = stream.stdout.decode('utf-8')
output = output.strip("\t").split("\n")
output.pop(3)
for item in output:
    logging.info(item)

for line in output:
    component = line.split(" ")[2]
    old = line.split(" ")[5]
    new = line.split(" ")[7].strip(")")

    if old.strip(" v.") < new.strip(" v."):
        body = body + f"New {component} version available {old} -> {new}\n"
        update_available = True

if body == '':
    logging.info("No new Update available")
    logging.info("**********************")
else:
    subject = "PiHole Update"
    sendmail(subject, body)
    logging.info("**********************")

