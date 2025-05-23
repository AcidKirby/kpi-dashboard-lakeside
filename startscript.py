# pip install sqlalchemy pymysql openpyxl


import pandas as pd
from sqlalchemy import create_engine
from datetime import timedelta

# --------------------
# CONFIGURATIE
# --------------------
bestand_excel = "besteldata.xlsx"
bestand_robot = "robot_restaurant_log.json"

host = "localhost"
port = 3306
database = "hr"
user = "kpidashboard"
password = "mand"

# --------------------
# DATABASE
# --------------------
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# --------------------
# INLEZEN MENSELIJKE DATA (EXCEL)
# --------------------
df_mens = pd.read_excel(bestand_excel)

# Tijdkolommen correct verwerken 
df_mens['Time_Order'] = pd.to_datetime(
    df_mens['Date'].dt.date.astype(str) + " " + df_mens['Time_Order'].astype(str),
    errors='coerce'
)
# Zorg dat Time_Ready en Time_Delivery goed zijn geparsed
# Voeg een datum toe aan tijdkolommen van menselijke data
df_mens['Time_Ready'] = pd.to_datetime(
    df_mens['Date'].dt.date.astype(str) + " " + df_mens['Time_Ready'].astype(str),
    errors='coerce'
)

df_mens['Time_Delivery'] = pd.to_datetime(
    df_mens['Date'].dt.date.astype(str) + " " + df_mens['Time_Delivery'].astype(str),
    errors='coerce'
)

# Datum en geboortedatum
df_mens['Date'] = pd.to_datetime(df_mens['Date'], errors='coerce')
df_mens['Birth_Date'] = pd.to_datetime(df_mens['Birth_Date'], errors='coerce')

# Leeftijd berekenen
df_mens['Leeftijd'] = ((pd.to_datetime("2025-05-01") - df_mens['Birth_Date']).dt.days / 365).astype(int)

# Dummydata voor kostenberekening
# (€500.000 / (20 medewerkers × 250 dagen) ≈ €100 per dag per medewerker)
# 6 uur × €15/u = €90 per dag per medewerker

df_mens['Uren'] = 6
df_mens['Uurtarief'] = 15

# --------------------
# INLEZEN ROBOTDATA (JSON)
# --------------------
df_robot = pd.read_json(bestand_robot)

df_robot['Date'] = pd.to_datetime(df_robot['Date'], format="%Y-%m-%d", errors='coerce')
df_robot['Birth_Date'] = pd.to_datetime(df_robot['Birth_Date'], format="%d-%m-%Y", errors='coerce')
df_robot['Time_Picked'] = pd.to_datetime(df_robot['Time_Picked'], format="%H:%M:%S", errors='coerce')
df_robot['Time_Delivery'] = pd.to_datetime(df_robot['Time_Delivery'], format="%H:%M:%S", errors='coerce')

df_robot['Age'] = ((df_robot['Date'] - df_robot['Birth_Date']).dt.days / 365).astype(int)
df_robot['Rating'] = pd.to_numeric(df_robot['Rating'], errors='coerce')
df_robot['Power consumption'] = pd.to_numeric(df_robot['Power consumption'], errors='coerce')



# --------------------
# KPI FUNCTIES
# --------------------
def kpi_klanttevredenheid_jong(df_mens, df_robot):
    mens_score = df_mens[df_mens['Leeftijd'] <= 45]['Rating'].mean()
    robot_score = df_robot[df_robot['Age'] <= 45]['Rating'].mean()
    print("\n📊 KPI: Klanttevredenheid jonge klanten (≤ 45 jaar)")
    print("Mens:", mens_score)
    print("Robot:", robot_score)
    return mens_score, robot_score



def kpi_fouten_per_dag(df_mens, df_robot):
    print("\n📊 KPI: Aantal fouten per dag (< 6 beoordeling)")

    # Filter data op alleen april t/m begin mei 2025
    start = "2025-04-22"
    end = "2025-05-05"

    fouten_mens = df_mens[df_mens['Rating'] < 6].groupby(df_mens['Date']).size()
    fouten_robot = df_robot[df_robot['Rating'] < 6].groupby(df_robot['Date']).size()

    fouten_mens_filtered = fouten_mens.loc[start:end]
    fouten_robot_filtered = fouten_robot.loc[start:end]

    print("Mens:\n", fouten_mens_filtered.to_string())
    print("Robot:\n", fouten_robot_filtered.to_string())

    return fouten_mens_filtered, fouten_robot_filtered


def kpi_bezorgsnelheid(df_mens, df_robot):
    print("\n📊 KPI: Gemiddelde bezorgtijd in seconden")

    # Voor menselijke bestellingen
    df_mens_clean = df_mens.dropna(subset=['Time_Ready', 'Time_Delivery']).copy()
    df_mens_clean['Bezorgtijd'] = (
        df_mens_clean['Time_Delivery'] - df_mens_clean['Time_Ready']
    ).dt.total_seconds()
    mens_bz = df_mens_clean['Bezorgtijd'].mean()

    # Voor robotbestellingen
    df_robot_clean = df_robot.dropna(subset=['Time_Picked', 'Time_Delivery']).copy()
    df_robot_clean['Bezorgtijd'] = (
        df_robot_clean['Time_Delivery'] - df_robot_clean['Time_Picked']
    ).dt.total_seconds()
    robot_bz = df_robot_clean['Bezorgtijd'].mean()

    print("Mens:", mens_bz)
    print("Robot:", robot_bz)

    return mens_bz, robot_bz



def kpi_orders_per_uur(df_mens, df_robot):
    print("\n📊 KPI: Aantal orders per uur (gemiddeld per dag)")

    df_mens_clean = df_mens.dropna(subset=['Time_Order']).copy()
    df_mens_clean['Uur'] = df_mens_clean['Time_Order'].dt.hour
    df_mens_clean['Datum'] = df_mens_clean['Date'].dt.date
    orders_mens = df_mens_clean.groupby(['Datum', 'Uur'])['Order_ID'].nunique().groupby('Uur').mean()

    df_robot_clean = df_robot.dropna(subset=['Time_Picked']).copy()
    df_robot_clean['Uur'] = df_robot_clean['Time_Picked'].dt.hour
    df_robot_clean['Datum'] = df_robot_clean['Date'].dt.date
    orders_robot = df_robot_clean.groupby(['Datum', 'Uur'])['Order_ID'].nunique().groupby('Uur').mean()

    print("Mens (gem. per dag):\n", orders_mens.round(2).to_string())
    print("Robot (gem. per dag):\n", orders_robot.round(2).to_string())

    return orders_mens, orders_robot

def kpi_kosten_per_dag(df_mens, df_robot):
    print("\n📊 KPI: Kosten per dag")

    df_mens['Kosten'] = df_mens['Uren'] * df_mens['Uurtarief']
    kosten_mens = df_mens.groupby(df_mens['Date'])['Kosten'].sum()

    kosten_robot = df_robot.groupby(df_robot['Date'])['Power consumption'].sum() * 0.32 + 695

    print("Mens:")
    print(kosten_mens.apply(lambda x: f"€{x:.2f}").to_string())

    print("Robot:")
    print(kosten_robot.apply(lambda x: f"€{x:.2f}").to_string())

    return kosten_mens, kosten_robot

def kpi_beschikbaarheid_totaal(beschikbaarheid_path: str, df_robot):
    df_beschikbaarheid = pd.read_csv(beschikbaarheid_path)
    mens_beschikbaarheid = df_beschikbaarheid["beschikbaarheid_percentage"].mean()

    df_robot["Date"] = pd.to_datetime(df_robot["Date"], format="%d-%m-%Y", errors="coerce")
    df_robot["Time_Picked"] = pd.to_datetime(df_robot["Time_Picked"], format="%H:%M:%S", errors="coerce")
    df_robot["DateTime_Picked"] = df_robot["Date"] + pd.to_timedelta(df_robot["Time_Picked"].dt.strftime('%H:%M:%S'))

    df_errors = df_robot[df_robot["Error_code"] != ""].copy()
    storing_duur = timedelta(0)

    for _, row in df_errors.iterrows():
        fouttijd = row["DateTime_Picked"]
        voor = df_robot[(df_robot["DateTime_Picked"] < fouttijd) & (df_robot["Error_code"] == "")]
        na = df_robot[(df_robot["DateTime_Picked"] > fouttijd) & (df_robot["Error_code"] == "")]
        if not voor.empty and not na.empty:
            storing_duur += na["DateTime_Picked"].min() - voor["DateTime_Picked"].max()

    werk_orders = df_robot[df_robot["Error_code"] == ""]
    totale_tijd = werk_orders["DateTime_Picked"].max() - werk_orders["DateTime_Picked"].min()
    robot_beschikbaarheid = round((1 - storing_duur / totale_tijd) * 100, 2)

    print(f"\n📊 KPI: Beschikbaarheid personeel")
    print(f"Mens: {mens_beschikbaarheid:.2f}%")
    print(f"Robot: {robot_beschikbaarheid:.2f}%")

    return mens_beschikbaarheid, robot_beschikbaarheid


# --------------------
# MAIN
# --------------------
def main():
    
    
 # Klanttevredenheid
    score_mens, score_robot = kpi_klanttevredenheid_jong(df_mens, df_robot)

    # Fouten per dag
    fouten_mens, fouten_robot = kpi_fouten_per_dag(df_mens, df_robot)

    # Bezorgtijd
    mens_bz, robot_bz = kpi_bezorgsnelheid(df_mens, df_robot)

    # Orders per uur
    orders_mens, orders_robot = kpi_orders_per_uur(df_mens, df_robot)

    # Kosten per dag
    kosten_mens, kosten_robot = kpi_kosten_per_dag(df_mens, df_robot)

    #Beschikbaarheid van bedienend personeel
    beschikbaarheid_mens, beschikbaarheid_robot = kpi_beschikbaarheid_totaal("KPI 6 - Beschikbaarheid(in).csv", df_robot)


    # ✅ Resultaten opslaan voor dashboard
    pd.DataFrame({
        "Klanttevredenheid_mens": [score_mens],
        "Klanttevredenheid_robot": [score_robot],
        "Bezorgtijd_mens": [mens_bz],
        "Bezorgtijd_robot": [robot_bz],
    }).to_csv("kpi_scores.csv", index=False)

    pd.DataFrame({
    "Beschikbaarheid_mens": [beschikbaarheid_mens],
    "Beschikbaarheid_robot": [beschikbaarheid_robot]
}).to_csv("beschikbaarheid.csv", index=False)

    fouten_mens.to_csv("fouten_mens.csv")
    fouten_robot.to_csv("fouten_robot.csv")
    orders_mens.to_csv("orders_mens.csv")
    orders_robot.to_csv("orders_robot.csv")
    kosten_mens.to_csv("kosten_mens.csv")
    kosten_robot.to_csv("kosten_robot.csv")

if __name__ == "__main__":
 main()