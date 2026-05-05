# ⚽ Simulador de Descenso - La Liga (Modelo Probabilístico PRO)

Simulador avanzado de probabilidades de descenso en La Liga basado en un modelo estadístico calibrado (Elo + Poisson) y simulaciones Monte Carlo.

---

## 🚀 Qué hace

- Simula miles de finales de liga en segundos
- Calcula probabilidades realistas de descenso
- Modela resultados partido a partido (no heurístico)
- Integra dinámica real de forma (racha automática vía Elo)
- Genera clasificación probabilística completa
- Permite análisis por equipo (escenarios, puntos necesarios)

---

## 🧠 Motor del modelo

Este simulador NO usa reglas simples. Está basado en un enfoque similar a modelos tipo FiveThirtyEight:

### 🔹 1. Rating dinámico (Elo)
- Cada equipo tiene un nivel de fuerza dinámico
- Se actualiza tras cada partido (real y simulado)
- Incluye:
  - ventaja de local
  - margen de victoria
  - rachas implícitas (forma real)

### 🔹 2. Probabilidades reales
- Probabilidad de victoria calculada con función logística:
`P(win) = 1 / (1 + 10^(-ΔElo / 400))`

### 🔹 3. Generación de goles (Poisson calibrado)
- Basado en medias reales del fútbol:
- ⚽ Local ≈ 1.43 goles
- ⚽ Visitante ≈ 1.12 goles
- Ajustado según la diferencia de nivel entre equipos

### 🔹 4. Simulación Monte Carlo
- Se repite la temporada miles de veces
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

✔ No depende de "últimos 5 partidos" artificiales  
✔ La forma se integra automáticamente vía Elo  
✔ Cada simulación evoluciona dinámicamente  
✔ Modelo coherente con fútbol real  
✔ Sensible a rachas, calendario y nivel  

---

## 🖥️ Aplicación interactiva

Incluye una app en Streamlit donde puedes:

- Ajustar número de simulaciones
- Analizar cualquier equipo
- Ver probabilidades en tiempo real
- Visualizar distribuciones de posiciones

---

## ▶️ Cómo ejecutar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt

### 2. Lanzar la app
```bash
streamlit run app.py
