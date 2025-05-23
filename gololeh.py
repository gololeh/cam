import os
import subprocess
import time
import re
import sys

# Create folder
if not os.path.exists("img"):
    os.mkdir("img")

# Start PHP server
php_server = subprocess.Popen(
    ["php", "-S", "localhost:8080"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

time.sleep(2)

# Create Serveo tunnel
sys.stdout.write("\n[*] Creating Serveo link...\n\n")
sys.stdout.flush()

serveo = subprocess.Popen(
    ["ssh", "-oStrictHostKeyChecking=no", "-R", "80:localhost:8080", "serveo.net"],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True
)

# Get URL
serveo_url = ""
while True:
    line = serveo.stdout.readline()
    if "Forwarding HTTP" in line:
        match = re.search(r"https://[^\s]+", line)
        if match:
            serveo_url = match.group().strip()
            sys.stdout.write("Link:\n")
            sys.stdout.write(f"{serveo_url}\n\n")
            sys.stdout.flush()
            break

# Monitor access
with open("access.log", "w") as f:
    pass

sys.stdout.write("[*] Waiting for user to access the link...\n\n")
sys.stdout.flush()

tail = subprocess.Popen(
    ["tail", "-f", "access.log"],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True
)

while True:
    output = tail.stdout.readline()
    if "GET / " in output or "GET /index.html" in output:
        sys.stdout.write("\nUser Entered\n\n")
        sys.stdout.flush()
        break
