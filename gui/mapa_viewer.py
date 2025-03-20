import os
import sqlite3
import folium
import pandas as pd
from folium.plugins import HeatMap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMessageBox


class MapaViewer(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.gerar_mapa("Todos", "Todos")

    def gerar_mapa(self, motorista, evento):
        conn = sqlite3.connect("../data/eventos.db")

        try:
            query = "SELECT Latitude, Longitude FROM eventos WHERE 1=1"
            params = []  # Lista para evitar SQL Injection e erros

            # aquele debug de preguiçoso maroto pra n perder o costume
            print(f"Selecionando motorista: {motorista}, evento: {evento}")

            if motorista != "Todos":
                query += " AND Motorista = ?"
                params.append(motorista)

            # confere no db se o CSV gerou a tabela de eventos ou botou tudo dentro de uma tabela só
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(eventos);")
            colunas = [col[1] for col in cursor.fetchall()]

            if "Evento" in colunas:
                if evento != "Todos":
                    query += " AND Evento LIKE ?"
# tira a concatenação de string pq mesmo sendo uma aplicação desktop eu ainda sou da cibersegurança e n quero SQL Injection aqui
                    params.append(evento)
            else:
                raise ValueError("A coluna de eventos não existe no banco de dados.")

            # outro debug pq o console ta ai pra isso, quando eu for compilar no PyInstaller eu tiro
            print(f"Query executada: {query}, com parâmetros: {params}")
            df = pd.read_sql(query, conn, params=params)

            # caixa de alerta ao tentar criar mapa vazio
            if df.empty:
                QMessageBox.warning(None, "Nenhum dado encontrado",
                                    "Nenhum evento encontrado para os filtros selecionados.")
                return

            # cria e centraliza o HeatMap com os filtros selecionados na query sequela(SQL)
            mapa = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=12)
            HeatMap(df.values).add_to(mapa)

            # salva o mapa e depois carrega ele no QWebEngineView
            mapa_path = os.path.abspath("../assets/mapa_calor.html")
            mapa.save(mapa_path)
            self.load(QUrl.fromLocalFile(mapa_path))

        # cria um balão de erro se der erro, mas é auto-explicativo tbm se vc n entendeu rapaz....
        except Exception as e:
            QMessageBox.critical(None, "Erro ao gerar mapa", f"Ocorreu um erro:\n{str(e)}")
            print(f"Erro ao gerar mapa: {e}")

        finally:
            conn.close()
