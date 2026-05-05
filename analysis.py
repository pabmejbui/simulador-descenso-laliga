"""
Módulo de análisis:
- Probabilidades de descenso
- Umbrales de salvación
- Dependencia de sí mismo
- Dependencias reales
"""
from collections import Counter

def analyze(simulations, team_name):
    total = len(simulations)

    relegated = 0
    points_when_safe = []
    all_points = []
    survival_cutoffs = []

    for sim in simulations:
        table = sim["table"]

        pos = table[team_name]["position"]
        pts = table[team_name]["points"]

        all_points.append(pts)

        if pos >= 18:
            relegated += 1
        else:
            points_when_safe.append(pts)

        # puntos del 17º
        for t, data in table.items():
            if data["position"] == 17:
                survival_cutoffs.append(data["points"])
                break

    prob_desc = relegated / total * 100

    min_points = min(points_when_safe) if points_when_safe else None

    # 🔥 CLAVE: +1
    guaranteed_safe_points = (max(survival_cutoffs) + 1) if survival_cutoffs else None

    threshold_90 = None

    for p in sorted(set(all_points)):
        cases = [sim for sim in simulations if sim["table"][team_name]["points"] >= p]

        if not cases:
            continue

        survival_rate = sum(
            1 for sim in cases if sim["table"][team_name]["position"] < 18
        ) / len(cases)

        if survival_rate >= 0.9:
            threshold_90 = p
            break

    return {
        "prob_descenso": prob_desc,
        "min_points_optimista": min_points,
        "min_points_90": threshold_90,
        "min_points_seguro": guaranteed_safe_points
    }


def depends_on_itself(teams, fixtures, team_name, N=20000):
    from simulator import simulate_season_forced

    relegated = 0

    for _ in range(N):
        sim = simulate_season_forced(teams, fixtures, team_name)

        if sim[team_name]["position"] >= 18:
            relegated += 1

    return relegated == 0


def dependency_needs_real(simulations, team_name, top_n=3):
    """
    Qué equipos deben fallar para salvarse
    """

    from collections import Counter

    combo_counter = Counter()

    for sim in simulations:
        table = sim["table"]

        if table[team_name]["position"] >= 18:

            sorted_table = sorted(table.items(), key=lambda x: x[1]["position"])

            # equipos que se salvan
            safe_teams = [t for t, data in sorted_table if data["position"] < 18]

            # zona crítica (últimos salvados)
            key_rivals = tuple(sorted(safe_teams[-3:]))

            combo_counter[key_rivals] += 1

    most_common = combo_counter.most_common(top_n)

    results = []

    for combo, _ in most_common:
        teams_str = ", ".join(combo)
        results.append(f"Que fallen varios de: {teams_str}")

    return results

def probabilistic_table(simulations, teams):

    position_data = {team: [] for team in teams}
    points_data = {team: [] for team in teams}

    for sim in simulations:
        table = sim["table"]

        for team in teams:
            position_data[team].append(table[team]["position"])
            points_data[team].append(table[team]["points"])

    results = {}

    for team in teams:
        positions = position_data[team]
        points = points_data[team]

        avg_pos = round(sum(positions) / len(positions), 2)

        pos_counter = Counter(positions)
        most_likely_pos = pos_counter.most_common(1)[0][0]

        points_counter = Counter(points)
        most_likely_points = points_counter.most_common(1)[0][0]  # 🔥 CLAVE

        distribution = {
            pos: round(count / len(positions) * 100, 2)
            for pos, count in pos_counter.items()
        }

        results[team] = {
            "avg_position": avg_pos,
            "most_likely_position": most_likely_pos,
            "most_likely_points": most_likely_points,  # 🔥 NUEVO
            "distribution": distribution
        }

    sorted_table = sorted(
        results.items(),
        key=lambda x: x[1]["avg_position"]
    )

    return sorted_table, results