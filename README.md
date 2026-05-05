# ⚽ Simulador de Descenso - La Liga (Modelo Probabilístico PRO)

Simulador avanzado de probabilidades de descenso en La Liga basado en un modelo estadístico calibrado (Elo + Poisson) y simulaciones Monte Carlo.

---

## 🚀 Qué hace

- Simula miles de finales de liga en segundos
- Calcula probabilidades realistas de descenso
- Modela resultados partido a partido (no heurístico)
- Integra dinámica real de forma (Elo dinámico)
- Genera clasificación probabilística completa
- Permite análisis por equipo (escenarios, puntos necesarios)

---

## 🧠 Motor del modelo

Este simulador NO usa reglas simples. Está basado en un enfoque similar a modelos tipo FiveThirtyEight:

### 🔹 1. Rating dinámico (Elo)

- Cada equipo tiene un nivel de fuerza dinámico
- Se actualiza tras cada partido (real y simulado)
- Incluye:
  - ventaja de local (~85 Elo)
  - margen de victoria
  - evolución de forma implícita

---

### 🔹 2. Probabilidades reales

Se calcula la probabilidad de victoria mediante una función logística:

`P(win) = 1 / (1 + 10^(-ΔElo / 400))`


---

### 🔹 3. Generación de goles (Poisson calibrado)

- Basado en medias reales del fútbol:
  - ⚽ Local ≈ 1.43 goles
  - ⚽ Visitante ≈ 1.12 goles
- Ajustado dinámicamente según la diferencia de nivel entre equipos

---

### 🔹 4. Simulación Monte Carlo

- Se repite la temporada miles de veces
- Cada simulación evoluciona de forma independiente
- Se obtiene una distribución completa de resultados

---

## 📊 Métricas

| Métrica | Descripción |
|--------|------------|
| 🔻 Descenso (%) | Probabilidad de acabar en puestos de descenso |
| 📊 Pos media | Posición media final |
| 🎯 Pos probable | Posición más frecuente |
| ⚽ Puntos probables | Puntos más probables |
| 🟢 Seguro | Puntos que garantizan salvación |
| 🟡 90% | Puntos con alta probabilidad de salvarse |
| 🔴 Mínimo | Escenario optimista |

---

## 🧩 Qué lo hace potente

✔ Modelo probabilístico realista  
✔ Evolución dinámica partido a partido  
✔ No depende de reglas artificiales  
✔ Sensible a nivel, calendario y resultados previos  
✔ Usa criterios reales de desempate (H2H)  

---

## 🖥️ Aplicación interactiva

Incluye una app en Streamlit donde puedes:

- Ajustar número de simulaciones
- Analizar cualquier equipo
- Ver probabilidades en tiempo real
- Visualizar distribuciones de posiciones

---