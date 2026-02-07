import requests
from datetime import datetime, timedelta
import pytz
import os

YEAR = 2026
OUTPUT_FILE = "f1_2026_brt.ics"

BRT = pytz.timezone("America/Sao_Paulo")
UTC = pytz.utc

ERGAST_URL = f"https://ergast.com/api/f1/{YEAR}.json"

os.makedirs(".", exist_ok=True)

def brt_datetime(date_str, time_str):
    dt_utc = UTC.localize(
        datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    )
    return dt_utc.astimezone(BRT)

response = requests.get(ERGAST_URL, timeout=30)
response.raise_for_status()

races = response.json()["MRData"]["RaceTable"]["Races"]

lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Motorsport Calendars//F1 2026//PT-BR",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "X-WR-CALNAME:Fórmula 1 2026 (BRT)",
    "X-WR-TIMEZONE:America/Sao_Paulo",
]

for race in races:
    race_name = race["raceName"]
    date = race["date"]
    time = race.get("time", "00:00:00").replace("Z", "")

    start = brt_datetime(date, time)
    end = start + timedelta(hours=2)

    uid = f"f1-2026-{race['round']}@motorsport"

    lines.extend([
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
        f"DTSTART;TZID=America/Sao_Paulo:{start.strftime('%Y%m%dT%H%M%S')}",
        f"DTEND;TZID=America/Sao_Paulo:{end.strftime('%Y%m%dT%H%M%S')}",
        f"SUMMARY:{race_name} - Fórmula 1",
        f"DESCRIPTION:Largada às {start.strftime('%H:%M')} (BRT)",
        "BEGIN:VALARM",
        "TRIGGER:-P1D",
        "ACTION:DISPLAY",
        "DESCRIPTION:Lembrete: corrida amanhã",
        "END:VALARM",
        "BEGIN:VALARM",
        "TRIGGER:-PT30M",
        "ACTION:DISPLAY",
        "DESCRIPTION:Lembrete: corrida em 30 minutos",
        "END:VALARM",
        "END:VEVENT",
    ])

lines.append("END:VCALENDAR")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Arquivo {OUTPUT_FILE} gerado com sucesso.")

