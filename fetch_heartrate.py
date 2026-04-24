import requests, json, time
from datetime import date, timedelta

TOKEN = "YOUR_TOKEN"  # 替换成你的 token
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
BASE = "https://api.ouraring.com"
OUT = "/Users/shipeifeng/Oura ring_Structuredataset_modeling/raw_data/heartrate.json"

start = date(2025, 9, 7)
end   = date(2026, 4, 13)
all_records = []

current = start
while current < end:
    next_day = current + timedelta(days=1)
    params = {
        "start_datetime": f"{current}T00:00:00",
        "end_datetime":   f"{next_day}T00:00:00"
    }
    resp = requests.get(f"{BASE}/v2/usercollection/heartrate", headers=HEADERS, params=params)
    if resp.status_code == 200:
        data = resp.json().get("data", [])
        all_records.extend(data)
        print(f"{current}: {len(data)} readings")
    else:
        print(f"{current}: ERROR {resp.status_code}")
    current = next_day
    time.sleep(0.3)

with open(OUT, "w") as f:
    json.dump({"data": all_records}, f, indent=2)

print(f"\nTotal: {len(all_records)} records saved.")
