from datetime import datetime

events = [
    ("GP da Austrália", "20260308T010000"),
    ("GP da China", "20260315T040000"),
    ("GP do Japão", "20260329T020000"),
    ("GP do Bahrein", "20260412T120000"),
    ("GP da Arábia Saudita", "20260419T140000"),
    ("GP de Miami", "20260503T160000"),
    ("GP do Canadá", "20260524T150000"),
    ("GP de Mônaco", "20260607T100000"),
    ("GP da Espanha (Barcelona)", "20260614T100000"),
    ("GP da Áustria", "20260628T100000"),
    ("GP do Reino Unido", "20260705T110000"),
    ("GP da Bélgica", "20260719T100000"),
    ("GP da Hungria", "20260726T100000"),
    ("GP da Holanda", "20260823T100000"),
    ("GP da Itália", "20260906T100000"),
    ("GP da Espanha (Madrid)", "20260913T100000"),
    ("GP do Azerbaijão", "20260927T080000"),
    ("GP de Singapura", "20261011T090000"),
    ("GP dos EUA (Austin)", "20261025T160000"),
    ("GP do México", "20261101T160000"),
    ("GP do Brasil", "20261108T140000"),
    ("GP de Las Vegas", "20261122T030000"),
    ("GP do Catar", "20261129T130000"),
    ("GP de Abu Dhabi", "20261206T100000"),
]

ics = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Motorsport Calendars//F1 2026 BRT//PT-BR
CALSCALE:GREGORIAN
METHOD:PUBLISH
TZID:America/Sao_Paulo

BEGIN:VTIMEZONE
TZID:America/Sao_Paulo
BEGIN:STANDARD
TZOFFSETFROM:-0300
TZOFFSETTO:-0300
TZNAME:BRT
DTSTART:19700101T000000
END:STANDARD
END:VTIMEZONE
"""

for i, (name, start) in enumerate(events, 1):
    ics += f"""
BEGIN:VEVENT
UID:f1-2026-{i}@github
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
DTSTART;TZID=America/Sao_Paulo:{start}
DTEND;TZID=America/Sao_Paulo:{start}
SUMMARY:Fórmula 1 2026 – {name}
DESCRIPTION:Largada da Fórmula 1 2026 em horário de Brasília.
BEGIN:VALARM
TRIGGER:-P1D
ACTION:DISPLAY
DESCRIPTION:F1 amanhã!
END:VALARM
BEGIN:VALARM
TRIGGER:-PT30M
ACTION:DISPLAY
DESCRIPTION:F1 em 30 minutos!
END:VALARM
END:VEVENT
"""

ics += "\nEND:VCALENDAR"

import os

os.makedirs("calendars", exist_ok=True)

with open("calendars/f1_2026_brt.ics", "w", encoding="utf-8") as f:
    f.write(ics)
