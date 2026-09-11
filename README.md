# X4 Calendar Tool

Tiny GitHub-side data source for the RoundedRaff X4 calendar.

## What it does

- Generates `today.json` every day using **Vietnam time (Asia/Ho_Chi_Minh)**.
- Calculates Vietnamese lunar date.
- Keeps owner information in `config/owner.json`.
- Lets the repository owner edit name / phone / email from GitHub Actions.
- Regenerates `today.json` after owner changes.
- Exposes one small JSON endpoint for the X4 firmware.

## Repository layout

```text
x4-calendar-tool/
├── today.json
├── config/
│   └── owner.json
├── scripts/
│   └── generate_calendar.py
└── .github/
    └── workflows/
        ├── generate-calendar.yml
        └── update-owner.yml
```

## Owner editing

Open:

**GitHub → Actions → Update owner information → Run workflow**

Enter any changed values. The workflow preserves a field when its input is left blank, then regenerates `today.json`.

No firmware reflashing is required.

## Daily generation

The scheduled workflow runs shortly after midnight Vietnam time. It can also be run manually.

GitHub Actions cron is UTC, so `05 17 * * *` means 00:05 in Vietnam during UTC+7.

## X4 endpoint

The firmware should fetch only:

```text
https://raw.githubusercontent.com/<OWNER>/<REPO>/main/today.json
```

Replace `<OWNER>/<REPO>` after creating the repository.

For GitHub Pages, the same file can alternatively be served from the Pages URL.

## JSON contract

```json
{
  "date": "2026-09-11",
  "calendar": {
    "day": 11,
    "month": 9,
    "weekday": 5,
    "lunar_day": 20,
    "lunar_month": 7
  },
  "owner": {
    "name": "",
    "phone": "",
    "email": ""
  }
}
```

`weekday` uses Python's Monday=1 ... Sunday=7 convention.

The generator uses the Vietnamese lunar-calendar calculation with UTC+7.

## Important privacy note

If this repository is public, `today.json` and `config/owner.json` are public. Do not put private information there unless you are comfortable exposing it.
