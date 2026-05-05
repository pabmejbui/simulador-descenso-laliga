import json
from simulator import simulate_season
from analysis import analyze, depends_on_itself, dependency_needs_real, probabilistic_table
from collections import Counter

# =========================
# 🔥 CARGAR DATOS
# =========================
with open("data/teams.json") as f:
    teams = json.load(f)

with open("data/matches.json") as f:
    past_results = json.load(f)

with open("data/fixtures.json") as f:
    fixtures = json.load(f)

# 🔥 DEBUG inicial
print("Partidos jugados:", len(past_results))
print("Partidos pendientes:", len(fixtures))

# =========================
# 🔥 PARTIDOS RESTANTES
# =========================
remaining_games = Counter()

for home, away in fixtures:
    remaining_games[home] += 1
    remaining_games[away] += 1

# =========================
# 🔥 SIMULACIÓN
# =========================
N = 100000
simulations = []

print("\nSimulando temporadas...\n")

for i in range(N):
    if i % 20000 == 0:
        print(f"Simulación {i}/{N}")
    simulations.append(simulate_season(teams, fixtures, past_results))

print("\n=== CLASIFICACIÓN PROBABILÍSTICA ===\n")

# =========================
# 🔥 CLASIFICACIÓN GLOBAL
# =========================
sorted_table, full_data = probabilistic_table(simulations, teams)

for i, (team, data) in enumerate(sorted_table, 1):
    print(f"{i}. {team}")
    print(f"   📊 Posición media: {data['avg_position']}")
    print(f"   🎯 Más probable: {data['most_likely_position']}")
    print(f"   ⚽ Puntos medios: {data['avg_points']}")

print("\n=== LUCHA POR EL DESCENSO ===\n")

# =========================
# 🔥 ANÁLISIS
# =========================
results_all = {}

for team in teams.keys():
    results_all[team] = analyze(simulations, team)

filtered = {
    team: res for team, res in results_all.items()
    if res["prob_descenso"] > 0.01
}

sorted_teams = sorted(filtered.items(), key=lambda x: x[1]["prob_descenso"], reverse=True)

# =========================
# 🔥 OUTPUT POR EQUIPO
# =========================
for team, res in sorted_teams:

    print(f"\n=== {team.upper()} ===")
    print(f"🔻 Descenso: {res['prob_descenso']}%")

    current = teams[team]["points"]
    max_points_left = remaining_games[team] * 3

    # 🔴 DESCENDIDO
    if res["prob_descenso"] == 100:
        print("❌ DESCENDIDO MATEMÁTICAMENTE")

    def calc_needed(total_points):
        if total_points is None:
            return None
        return max(0, total_points - current)

    needed_safe = calc_needed(res["min_points_seguro"])
    needed_90 = calc_needed(res["min_points_90"])
    needed_opt = calc_needed(res["min_points_optimista"])

    # 🟢 SALVACIÓN SEGURA
    if needed_safe is not None:
        if needed_safe > max_points_left:
            print(f"🟥 Ni ganando {max_points_left}/{max_points_left} puntos se salva seguro")
        else:
            print(f"🟢 Necesita {needed_safe}/{max_points_left} puntos para salvarse seguro")

    # 🟡 90%
    if needed_90 is not None:
        print(f"🟡 Con {needed_90}/{max_points_left} puntos tiene ~90% de salvarse")

    # 🔴 MÍNIMO
    if needed_opt is not None:
        print(f"🔴 Puede salvarse incluso con {needed_opt}/{max_points_left} puntos")

    # =========================
    # 🔥 DEPENDENCIAS
    # =========================
    depends = depends_on_itself(teams, fixtures, team, N=3000)

    print("\nDEPENDENCIAS:")

    if depends:
        print("🟢 Depende de sí mismo")
    else:
        print("🔴 No depende de sí mismo")

        deps = dependency_needs_real(simulations, team)

        for d in deps:
            print(f"   - {d}")