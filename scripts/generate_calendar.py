#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import vnlunar

ROOT = Path(__file__).resolve().parents[1]
OWNER_PATH = ROOT / "config" / "owner.json"
OUTPUT_PATH = ROOT / "today.json"

TZ = ZoneInfo("Asia/Ho_Chi_Minh")

WEEKDAYS = {
    0: "THỨ HAI",
    1: "THỨ BA",
    2: "THỨ TƯ",
    3: "THỨ NĂM",
    4: "THỨ SÁU",
    5: "THỨ BẢY",
    6: "CHỦ NHẬT",
}


def load_owner():
    if not OWNER_PATH.exists():
        return {"name": "", "phone": "", "email": ""}

    with OWNER_PATH.open("r", encoding="utf-8") as f:
        owner = json.load(f)

    if not isinstance(owner, dict):
        raise ValueError("owner.json must contain an object")

    return {
        "name": str(owner.get("name", "")).strip(),
        "phone": str(owner.get("phone", "")).strip(),
        "email": str(owner.get("email", "")).strip(),
    }


def generate():
    now = datetime.now(TZ)
    day = now.day
    month = now.month
    year = now.year

    lunar = vnlunar.get_lunar_date(day, month, year)

    result = {
        "date": now.strftime("%Y-%m-%d"),
        "calendar": {
            "day": day,
            "month": month,
            "weekday": now.isoweekday(),
            "weekday_text": WEEKDAYS[now.weekday()],
            "lunar_day": int(lunar["day"]),
            "lunar_month": int(lunar["month"]),
        },
        "owner": load_owner(),
    }

    # Keep the output deliberately small and stable for the X4.
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    generate()
