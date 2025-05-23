import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------
# Inlezen van data
# -----------------------
kpi = pd.read_csv("kpi_scores.csv")
fouten_mens = pd.read_csv("fouten_mens.csv", index_col=0, parse_dates=True)
fouten_robot = pd.read_csv("fouten_robot.csv", index_col=0, parse_dates=True)
orders_mens = pd.read_csv("orders_mens.csv", index_col=0)
orders_robot = pd.read_csv("orders_robot.csv", index_col=0)
kosten_mens = pd.read_csv("kosten_mens.csv", index_col=0)
kosten_robot = pd.read_csv("kosten_robot.csv", index_col=0)
beschikbaarheid = pd.read_csv("beschikbaarheid.csv")

# -----------------------
# Pagina instellingen
# -----------------------
st.set_page_config(layout="wide")
st.title("📊 KPI Dashboard – Lake Side Mania")

# -----------------------
# KPI: Klanttevredenheid jong - grafiek
# -----------------------
st.subheader("Klanttevredenheid jonge klanten (grafiek)")
fig_k1, ax_k1 = plt.subplots(figsize=(5, 3))
ax_k1.bar(["Mens", "Robot"], 
          [kpi['Klanttevredenheid_mens'][0], kpi['Klanttevredenheid_robot'][0]], 
          color=["#1f77b4", "#ff7f0e"])
ax_k1.axhline(7.00, color='gray', linestyle='--', label='Norm (7.00)')
ax_k1.set_ylabel("Gemiddelde beoordeling")
ax_k1.set_title("Klanttevredenheid (≤ 45 jaar)")
st.pyplot(fig_k1)

# -----------------------
# KPI: Bezorgsnelheid - grafiek
# -----------------------
st.subheader("Gemiddelde bezorgtijd (grafiek)")
fig_k2, ax_k2 = plt.subplots(figsize=(5, 3))
ax_k2.bar(["Mens", "Robot"], 
          [kpi['Bezorgtijd_mens'][0], kpi['Bezorgtijd_robot'][0]], 
          color=["#2ca02c", "#d62728"])
ax_k2.axhline(165.00, color='gray', linestyle='--', label='Norm (165s)')
ax_k2.set_ylabel("Tijd (in seconden)")
ax_k2.set_title("Gemiddelde bezorgtijd")
st.pyplot(fig_k2)
# -----------------------
# KPI: Fouten per dag
# -----------------------
start = "2025-04-22"
end = "2025-05-05"

fouten_mens_filtered = fouten_mens.loc[start:end]
fouten_robot_filtered = fouten_robot.loc[start:end]
st.subheader("Aantal fouten per dag")
fig1, ax1 = plt.subplots(figsize=(10, 4))
plt.plot(fouten_mens_filtered.index, fouten_mens_filtered.values, label='Mens', marker='o')
plt.plot(fouten_robot_filtered.index, fouten_robot_filtered.values, label='Robot', marker='s')
ax1.axhline(2, color='gray', linestyle='--', label='Norm (2 fouten)')
ax1.set_xlabel("Datum")
ax1.set_ylabel("Aantal fouten (<6 beoordeling)")
ax1.set_title("Aantal fouten per dag")
ax1.legend()
ax1.tick_params(axis='x', rotation=45)
st.pyplot(fig1)

# -----------------------
# KPI: Orders per uur
# -----------------------
st.subheader("Aantal orders per uur")
df_orders = pd.DataFrame({
    "Mens": orders_mens.squeeze(),
    "Robot": orders_robot.squeeze()
}).fillna(0)
fig2, ax2 = plt.subplots(figsize=(10, 4))
df_orders.plot(kind='bar', ax=ax2)
ax2.axhline(13, color='gray', linestyle='--', label='Norm (13 orders)')
ax2.set_ylabel("Aantal orders")
ax2.set_xlabel("Uur")
ax2.set_title("Aantal orders per uur")
ax2.legend()
st.pyplot(fig2)

# -----------------------
# KPI: Kosten per dag
# -----------------------
st.subheader("Kosten per dag (€)")
df_kosten = pd.DataFrame({
    "Mens": kosten_mens.squeeze(),
    "Robot": kosten_robot.squeeze()
}).fillna(0)
st.line_chart(df_kosten)

# -----------------------
# KPI: Beschikbaarheid (grafiek)
# -----------------------
st.subheader("Beschikbaarheid van personeel (%) – Mens vs Robot")

# Zet de beschikbaarheidsgegevens in de juiste vorm
beschikbaarheid_data = pd.DataFrame({
    "Type": ["Mens", "Robot"],
    "Beschikbaarheid": [
        beschikbaarheid["Beschikbaarheid_mens"].iloc[0],
        beschikbaarheid["Beschikbaarheid_robot"].iloc[0]
    ]
})

# Plot de grafiek
fig_beschikbaarheid, ax_beschikbaarheid = plt.subplots(figsize=(4, 3))
ax_beschikbaarheid.bar(
    beschikbaarheid_data["Type"],
    beschikbaarheid_data["Beschikbaarheid"],
    color=["#1f77b4", "#ff7f0e"]
)
ax_beschikbaarheid.set_ylim(0, 100)
ax_beschikbaarheid.set_ylabel("Beschikbaarheid (%)")
ax_beschikbaarheid.set_title("Personeelsbeschikbaarheid")
for i, v in enumerate(beschikbaarheid_data["Beschikbaarheid"]):
    ax_beschikbaarheid.text(i, v + 1, f"{v:.1f}%", ha='center')

st.pyplot(fig_beschikbaarheid)

# -----------------------
# Footer
# -----------------------
st.caption("Opdracht DP22 – KPI-dashboard | Gemaakt met ❤️ in Streamlit")
