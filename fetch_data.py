import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

headers = {
    "X-Auth-Token": API_KEY
}

BASE_URL = "https://api.football-data.org/v4/competitions/PD"

# =========================
# 🔥 MAPA DE NOMBRES
# =========================
name_map = {
    # TOP
    "FC Barcelona": "Barcelona",
    "Real Madrid CF": "Real Madrid",
    "Villarreal CF": "Villarreal",

    # ⚠️ CLAVE (añadir ESTE)
    "Atlético de Madrid": "Atletico",
    "Club Atlético de Madrid": "Atletico",

    # resto
    "Real Betis Balompié": "Betis",
    "RC Celta de Vigo": "Celta",
    "Getafe CF": "Getafe",
    "Athletic Club": "Athletic",
    "Real Sociedad de Fútbol": "Real Sociedad",
    "CA Osasuna": "Osasuna",
    "Rayo Vallecano de Madrid": "Rayo",
    "Valencia CF": "Valencia",
    "RCD Espanyol de Barcelona": "Espanyol",
    "Elche CF": "Elche",
    "RCD Mallorca": "Mallorca",
    "Girona FC": "Girona",
    "Sevilla FC": "Sevilla",
    "Deportivo Alavés": "Alaves",
    "Levante UD": "Levante",
    "Real Oviedo": "Oviedo"
}

os.makedirs("data", exist_ok=True)

# =========================
# 🔥 PARTIDOS JUGADOS
# =========================
print("Descargando partidos jugados...")

res = requests.get(f"{BASE_URL}/matches?status=FINISHED", headers=headers)
data = res.json()

matches = []

for m in data["matches"]:
    hg = m["score"]["fullTime"]["home"]
    ag = m["score"]["fullTime"]["away"]

    if hg is None or ag is None:
        continue

    home = name_map.get(m["homeTeam"]["name"], m["homeTeam"]["name"])
    away = name_map.get(m["awayTeam"]["name"], m["awayTeam"]["name"])

    matches.append([home, away, hg, ag])

with open("data/matches.json", "w") as f:
    json.dump(matches, f, indent=2)

print("✅ matches.json listo")

# =========================
# 🔥 PARTIDOS PENDIENTES
# =========================
print("Descargando partidos pendientes...")

res = requests.get(f"{BASE_URL}/matches?status=SCHEDULED", headers=headers)
data = res.json()

fixtures = []

for m in data["matches"]:
    home = name_map.get(m["homeTeam"]["name"], m["homeTeam"]["name"])
    away = name_map.get(m["awayTeam"]["name"], m["awayTeam"]["name"])

    fixtures.append([home, away])

with open("data/fixtures.json", "w") as f:
    json.dump(fixtures, f, indent=2)

print("✅ fixtures.json listo")

# =========================
# 🔥 CLASIFICACIÓN
# =========================
print("Descargando clasificación...")

res = requests.get(f"{BASE_URL}/standings", headers=headers)
data = res.json()

teams = {}

for t in data["standings"][0]["table"]:
    name = name_map.get(t["team"]["name"], t["team"]["name"])

    teams[name] = {
        "points": t["points"],
        "gf": t["goalsFor"],
        "ga": t["goalsAgainst"]
    }

with open("data/teams.json", "w") as f:
    json.dump(teams, f, indent=2)

print("✅ teams.json listo")