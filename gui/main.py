import sys
import os
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel
from mapa_viewer import MapaViewer


def preparar_dados():
    print("Processando dados...")
    os.system("python ../scripts/processar_dados.py")
    print("Dados processados.")

    print("Gerando mapa de calor...")
    os.system("python ../scripts/gerar_mapa.py")
    print("Mapa gerado.")

class MapaCalorApp(QWidget):
    def __init__(self):
        super().__init__()

        # Layout da interface
        self.setWindowTitle("Mapa de Calor Telemetria - Viação Ubá")
        self.setGeometry(100, 100, 1280, 720)
        layout = QVBoxLayout()

        # lista suspensa de motorista
        self.motorista_select = QComboBox(self)
        self.motorista_select.addItem("Todos")
        self.carregar_motoristas()
        layout.addWidget(QLabel("Selecionar Motorista:"))
        layout.addWidget(self.motorista_select)

        # lista suspensa de evento
        self.evento_select = QComboBox(self)
        self.evento_select.addItem("Todos")
        self.evento_select.addItems(["FAIXA VERMELHA", "FAIXA AMARELA"])
        layout.addWidget(QLabel("Selecionar Evento:"))
        layout.addWidget(self.evento_select)

        # f5 no mapa pra ficar bonitin
        self.btn_atualizar = QPushButton("Gerar Mapa de Calor")
        self.btn_atualizar.clicked.connect(self.atualizar_mapa)
        layout.addWidget(self.btn_atualizar)
        self.mapa_viewer = MapaViewer()
        layout.addWidget(self.mapa_viewer)

        self.setLayout(layout)

    def carregar_motoristas(self):
        conn = sqlite3.connect("../data/eventos.db")
        df = pd.read_sql("SELECT DISTINCT Motorista FROM eventos", conn)
        conn.close()
        for motorista in df["Motorista"]:
            self.motorista_select.addItem(motorista)

    def atualizar_mapa(self):
        motorista = self.motorista_select.currentText()
        evento = self.evento_select.currentText()
        self.mapa_viewer.gerar_mapa(motorista, evento)

if __name__ == "__main__":
    # prepara os dados antes de iniciar o app
    preparar_dados()

    # inicia a porra toda
    app = QApplication(sys.argv)
    janela = MapaCalorApp()
    janela.show()
    sys.exit(app.exec_())
