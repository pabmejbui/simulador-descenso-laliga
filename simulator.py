import random
import copy
import math
from collections import defaultdict
from utils import sort_table_with_h2h


# =========================
# 🔥 CONFIG REALISTA
# =========================
BASE_ELO = 1500
K = 20
HOME_ADV_ELO = 85

AVG_HOME_GOALS = 1.43
AVG_AWAY_GOALS = 1.12


# =========================
# 🔥 INIT ELO
# =========================
def init_elo(teams):
    return {
        team: BASE_ELO + data["points"] * 1.5
        for team, data in teams.items()
    }


# =========================
# 🔥 PROBABILIDAD ELO
# =========================
def win_probability(elo_home, elo_away):
    return 1 / (1 + 10 ** ((elo_away - elo_home) / 400))


# =========================
# 🔥 FORMA RECIENTE
# =========================
def build_form(past_results):
    form = defaultdict(list)

    for home, away, hg, ag in past_results:
        if hg > ag:
            form[home].append(3)
            form[away].append(0)
        elif ag > hg:
            form[home].append(0)
            form[away].append(3)
        else:
            form[home].append(1)
            form[away].append(1)

    for team in form:
        form[team] = form[team][-5:]

    return form


def form_factor(form, team):
    if team not in form or not form[team]:
        return 1.0

    avg = sum(form[team]) / (3 * len(form[team]))  # 0–1

    return 0.7 + 0.6 * avg  # rango: 0.7 – 1.3


# =========================
# 🔥 POISSON
# =========================
def poisson(lmbda):
    L = math.exp(-lmbda)
    k = 0
    p = 1

    while p > L:
        k += 1
        p *= random.random()

    return k - 1


# =========================
# 🔥 GOLES DESDE ELO
# =========================
def goals_from_prob(p_home):

    strength_factor = (p_home - 0.5) * 2  # [-1, 1]

    home_lambda = AVG_HOME_GOALS * (1 + 0.6 * strength_factor)
    away_lambda = AVG_AWAY_GOALS * (1 - 0.6 * strength_factor)

    return max(0.2, home_lambda), max(0.2, away_lambda)


# =========================
# 🔥 UPDATE ELO
# =========================
def update_elo(elo, home, away, hg, ag):

    elo_home = elo[home] + HOME_ADV_ELO
    elo_away = elo[away]

    expected_home = win_probability(elo_home, elo_away)

    # resultado real
    if hg > ag:
        result = 1
    elif hg < ag:
        result = 0
    else:
        result = 0.5

    # margen de victoria
    goal_diff = abs(hg - ag)
    margin_multiplier = math.log(goal_diff + 1) + 1

    elo[home] += K * margin_multiplier * (result - expected_home)
    elo[away] += K * margin_multiplier * ((1 - result) - (1 - expected_home))


# =========================
# 🔥 FIXTURES
# =========================
def get_remaining_fixtures(fixtures, past_results):
    played = set()

    if past_results:
        for home, away, _, _ in past_results:
            played.add((home, away))

    return [(h, a) for h, a in fixtures if (h, a) not in played]


# =========================
# 🔥 SIMULACIÓN FINAL
# =========================
def simulate_season(teams, fixtures, past_results=None):

    table = copy.deepcopy(teams)
    matches = []
    elo = init_elo(teams)

    # 🔥 FORMA
    form = build_form(past_results or [])

    # =========================
    # 🔥 USAR HISTÓRICO (SIN DUPLICAR)
    # =========================
    if past_results:
        for home, away, hg, ag in past_results:

            matches.append((home, away, hg, ag))

            # ❗ SOLO ELO (NO sumar puntos otra vez)
            update_elo(elo, home, away, hg, ag)

    remaining = get_remaining_fixtures(fixtures, past_results)

    # =========================
    # 🔥 SIMULAR FUTURO
    # =========================
    for home, away in remaining:

        elo_home = (elo[home] + HOME_ADV_ELO) * form_factor(form, home)
        elo_away = elo[away] * form_factor(form, away)

        p_home = win_probability(elo_home, elo_away)

        lam_home, lam_away = goals_from_prob(p_home)

        # 🔥 aplicar forma
        lam_home *= form_factor(form, home)
        lam_away *= form_factor(form, away)

        hg = poisson(lam_home)
        ag = poisson(lam_away)

        matches.append((home, away, hg, ag))

        # stats simulados
        table[home]["gf"] += hg
        table[home]["ga"] += ag
        table[away]["gf"] += ag
        table[away]["ga"] += hg

        if hg > ag:
            table[home]["points"] += 3
        elif ag > hg:
            table[away]["points"] += 3
        else:
            table[home]["points"] += 1
            table[away]["points"] += 1

        update_elo(elo, home, away, hg, ag)

    # =========================
    # 🔥 H2H
    # =========================
    h2h = {}

    for home, away, hg, ag in matches:

        key = tuple(sorted([home, away]))

        if key not in h2h:
            h2h[key] = {
                home: {"points": 0, "gd": 0},
                away: {"points": 0, "gd": 0}
            }

        h2h[key][home]["gd"] += (hg - ag)
        h2h[key][away]["gd"] += (ag - hg)

        if hg > ag:
            h2h[key][home]["points"] += 3
        elif ag > hg:
            h2h[key][away]["points"] += 3
        else:
            h2h[key][home]["points"] += 1
            h2h[key][away]["points"] += 1

    sorted_table = sort_table_with_h2h(table, h2h)

    final_positions = {}

    for i, (team, stats) in enumerate(sorted_table):
        final_positions[team] = {
            "position": i + 1,
            "points": stats["points"]
        }

    return {
        "table": final_positions,
        "matches": matches
    }