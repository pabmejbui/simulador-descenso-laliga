import streamlit as st
import json
import pandas as pd
from collections import Counter

from simulator import simulate_season
from analysis import analyze, probabilistic_table

st.set_page_config(layout="wide")

if st.sidebar.button("🧹 Limpiar caché"):
    st.cache_data.clear()
    st.rerun()

# =========================
# 🔥 LOAD DATA (CACHE)
# =========================
@st.cache_data
def load_data():
    with open("data/teams.json") as f:
        teams = json.load(f)

    with open("data/matches.json") as f:
        past_results = json.load(f)

    with open("data/fixtures.json") as f:
        fixtures = json.load(f)

    return teams, past_results, fixtures


# =========================
# 🔥 SIMULATION
# =========================
@st.cache_data(show_spinner=False)
def run_simulations(teams, fixtures, past_results, N):
    return [
        simulate_season(teams, fixtures, past_results)
        for _ in range(N)
    ]


# =========================
# 🔥 FORMAT PROBABILITY
# =========================
def format_prob(x, N):
    min_prob = 100 / N

    if x == 0:
        return f"<{min_prob:.2f}%"
    elif x < min_prob:
        return f"<{min_prob:.2f}%"
    else:
        return f"{x:.2f}%"


# =========================
# 🔥 LOAD
# =========================
teams, past_results, fixtures = load_data()

# =========================
# 🔥 SESSION STATE
# =========================
if "simulations" not in st.session_state:
    st.session_state.simulations = None
    st.session_state.last_N = None

# =========================
# 🔥 SIDEBAR
# =========================
st.sidebar.title("⚙️ Configuración")

N = st.sidebar.slider(
    "Número de simulaciones",
    1000, 50000, 10000, 1000,
    key="sim_slider"
)

selected_team = st.sidebar.selectbox(
    "Selecciona equipo",
    list(teams.keys()),
    key="team_select"
)

col1, col2 = st.sidebar.columns(2)
run_button = col1.button("🚀 Simular")
reuse_button = col2.button("♻️ Reusar")

# =========================
# 🔥 HEADER
# =========================
st.title("📊 Simulador La Liga - Descenso")

st.write(f"Partidos jugados: {len(past_results)}")
st.write(f"Partidos pendientes: {len(fixtures)}")

# =========================
# 🔥 CONTROL EJECUCIÓN
# =========================
if run_button or (
    reuse_button and st.session_state.simulations is not None
):

    if run_button or st.session_state.last_N != N:

        with st.spinner("Simulando temporadas..."):
            simulations = run_simulations(
                teams, fixtures, past_results, N
            )

        st.session_state.simulations = simulations
        st.session_state.last_N = N

    else:
        simulations = st.session_state.simulations

    st.success("Simulación lista")

    # =========================
    # 🔥 RESULTADOS
    # =========================
    sorted_table, full_data = probabilistic_table(simulations, teams)
    results = {team: analyze(simulations, team) for team in teams}

    # =========================
    # 🔥 TABLA PRO
    # =========================
    st.subheader("📊 Clasificación probabilística")

    df = pd.DataFrame([
        {
            "Equipo": team,
            "Pos media": round(data["avg_position"], 2),
            "Pos probable": data["most_likely_position"],
            "Pts probables": data["most_likely_points"],
            "Descenso %": results[team]["prob_descenso"]
        }
        for team, data in sorted_table
    ])

    df.index = df.index + 1

    # ✅ formato correcto
    df["Descenso %"] = df["Descenso %"].apply(lambda x: format_prob(x, N))

    st.dataframe(df, width="stretch")

    # =========================
    # 🔥 GRÁFICA DESCENSO
    # =========================
    st.subheader("🔻 Probabilidad de descenso")

    df_desc = pd.DataFrame([
        {"Equipo": t, "Descenso": results[t]["prob_descenso"]}
        for t in teams
    ]).sort_values("Descenso", ascending=False)

    st.bar_chart(df_desc.set_index("Equipo"), width="stretch")

    # =========================
    # 🔥 EQUIPO
    # =========================
    st.subheader(f"🔎 {selected_team}")

    res = results[selected_team]
    st.metric("Prob descenso", format_prob(res["prob_descenso"], N))

    current = teams[selected_team]["points"]

    remaining = Counter()
    for h, a in fixtures:
        remaining[h] += 1
        remaining[a] += 1

    max_points_left = remaining[selected_team] * 3

    def calc_needed(total):
        return None if total is None else max(0, total - current)

    st.write("### 🧮 Escenarios")

    safe = calc_needed(res["min_points_seguro"])
    p90 = calc_needed(res["min_points_90"])
    opt = calc_needed(res["min_points_optimista"])

    if safe is not None:
        st.write(f"🟢 Seguro: {safe}/{max_points_left}")
    if p90 is not None:
        st.write(f"🟡 90%: {p90}/{max_points_left}")
    if opt is not None:
        st.write(f"🔴 Mínimo: {opt}/{max_points_left}")

    # =========================
    # 🔥 DISTRIBUCIÓN
    # =========================
    st.subheader("📈 Distribución posiciones")

    dist = full_data[selected_team]["distribution"]

    df_dist = pd.DataFrame({
        "Posición": list(dist.keys()),
        "Probabilidad": list(dist.values())
    }).sort_values("Posición")

    st.bar_chart(df_dist.set_index("Posición"), width="stretch")