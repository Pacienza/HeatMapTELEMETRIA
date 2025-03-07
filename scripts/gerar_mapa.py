import folium
from folium.plugins import HeatMap
import sqlite3
import pandas as pd


conn = sqlite3.connect("../data/eventos.db")

# query de consulta no db
df = pd.read_sql("SELECT Latitude, Longitude FROM eventos", conn)
conn.close()

# centraliza o mapa aonde tem mais eventos e adiciona a parte do calor
m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=12)
HeatMap(df.values).add_to(m)

m.save("../assets/mapa_calor.html")

print("Mapa de calor gerado com sucesso!")
