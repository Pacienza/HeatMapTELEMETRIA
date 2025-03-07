import pandas as pd
import sqlite3

# transforma a a planilha CSV em DataFrame do Pandas
# https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
df = pd.read_csv("../data/baseCSV.csv", sep=";", encoding="utf-8")

# conecta com o sqlite e salva as parada no banco de dados
conn = sqlite3.connect("../data/eventos.db")
df.to_sql("eventos", conn, if_exists="replace", index=False)
conn.close()

print("Dados importados com sucesso!")
