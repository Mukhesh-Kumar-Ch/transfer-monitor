import os
import json
import hashlib
import requests
from bs4 import BeautifulSoup

URL = "https://apche-transfers.aptonline.in/APCCETransfers/"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

STATE_FILE = "state.json"


def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg,
        },
        timeout=20,
        verify=False
    )

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

response = requests.get(
    URL,
    timeout=30,
    verify=False
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Remove scripts/styles
for tag in soup(["script", "style"]):
    tag.decompose()

text = soup.get_text(separator=" ", strip=True)

current_hash = hashlib.sha256(text.encode()).hexdigest()

if os.path.exists(STATE_FILE):
    with open(STATE_FILE) as f:
        state = json.load(f)
else:
    state = {}

previous_hash = state.get("hash")

if previous_hash is None:
    print("First run. Saving page.")
elif previous_hash != current_hash:
    send(
        "🚨 APCCE Transfer website changed!\n\n"
        "https://apche-transfers.aptonline.in/APCCETransfers/"
    )

state["hash"] = current_hash

with open(STATE_FILE, "w") as f:
    json.dump(state, f)

print("Done.")