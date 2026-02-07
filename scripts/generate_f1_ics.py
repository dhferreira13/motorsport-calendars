import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import sys

URL = "https://ergast.com/api/f1/2026.json"
OUTPUT_FILE = "f1_2026_brt.ics"

response = requests.get(URL, timeout=20)

# Se não houver JSON válido, apenas sair sem erro
if (
    response.status_code != 200
    or not response.headers.get("Content-Type", "").startswith("application/json")
):
    print("ℹ️ Calendário F1 2026 ainda não disponível. Nenhuma atualização feita.")
    sys.exit(0)

data = response.json()

races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])

if not races:
    print("ℹ️ Nenhuma corrida encontrada para F1 2026 ainda.")
    sys.exit(0)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("BEGIN:VCALENDAR\n")
    f.write("VERSION:2.0\n")
    f.write("PRODID:-//F1 2026 BRT//EN\n")
    f.write("CALSCALE:GREGORIAN\n")

    for race in races:
        race_name = race["raceName"]
        race_date = race["date"]
        race_time = race.get("time", "14:00:00Z")

        utc_dt = datetime.fromisoformat(
            f"{race_date}T{race_time.replace('Z','')}"
        ).replace(tzinfo=ZoneInfo("UTC"))

        brt_dt = utc_dt.astimezone(ZoneInfo("America/Sao_Paulo"))
        end_dt = brt_dt + timedelta(hours=2)

        uid = f"f1-2026-{race['round']}@motorsport-calendars"

        f.write("BEGIN:VEVENT\n")
        f.write(f"UID:{uid}\n")
        f.write(f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}\n")
        f.write(f"DTSTART:{brt_dt.strftime('%Y%m%dT%H%M%S')}\n")
        f.write(f"DTEND:{end_dt.strftime('%Y%m%dT%H%M%S')}\n")
        f.write(f"SUMMARY:F1 2026 – {race_name}\n")
        f.write("DESCRIPTION:Corrida da Fórmula 1 (horário BRT)\n")

        f.write("BEGIN:VALARM\n")
        f.write("TRIGGER:-P1D\n")
        f.write("ACTION:DISPLAY\n")
        f.write("DESCRIPTION:Lembrete: corrida amanhã\n")
        f.write("END:VALARM\n")

        f.write("BEGIN:VALARM\n")
        f.write("TRIGGER:-PT30M\n")
        f.write("ACTION:DISPLAY\n")
        f.write("DESCRIPTION:Lembrete: corrida em 30 minutos\n")
        f.write("END:VALARM\n")

        f.write("END:VEVENT\n")

    f.write("END:VCALENDAR\n")

print("✅ Calendário F1 2026 atualizado com sucesso.")



