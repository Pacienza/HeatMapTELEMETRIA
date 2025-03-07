import sys
import os
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QGridLayout, \
    QSpacerItem, QSizePolicy, QHBoxLayout
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
        self.setWindowTitle("Mapa de Calor Telemetria - Viação Ubá | Grupo CSC")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #138275;")

        # criação dos layouts a parte CSS grid (som de vomito) do bagulho
        layout_principal = QVBoxLayout()
        layout_filtros = QGridLayout()

        # lista suspensa de motorista
        self.motorista_select = QComboBox(self)
        self.motorista_select.addItem("Todos")
        self.motorista_select.setStyleSheet("background-color: white; color: black;")
        self.carregar_motoristas()
        layout_filtros.addWidget(QLabel("Selecionar Motorista:"), 0, 0)
        layout_filtros.addWidget(self.motorista_select, 0, 1)

        # lista suspensa de evento
        self.evento_select = QComboBox(self)
        self.evento_select.addItem("Todos")
        self.evento_select.addItems(["FAIXA VERMELHA", "FAIXA AMARELA"])
        self.evento_select.setStyleSheet("background-color: white; color: black;")
        layout_filtros.addWidget(QLabel("Selecionar Evento:"), 1, 0)
        layout_filtros.addWidget(self.evento_select, 1, 1)

        layout_principal.addLayout(layout_filtros)

        # Z-index do Qt5, evita sobreposição dos Widgets
        layout_principal.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))


        # botão pra dar f5 no mapa pra ficar bonitin
        self.btn_atualizar = QPushButton("Gerar Mapa de Calor")
        self.btn_atualizar.setStyleSheet("background-color: white; color: black;")
        self.btn_atualizar.clicked.connect(self.atualizar_mapa)
        layout_principal.addWidget(self.btn_atualizar)

        # visualização do mapa
        self.mapa_viewer = MapaViewer()
        layout_principal.addWidget(self.mapa_viewer, stretch=1)

        self.setLayout(layout_principal)

        # footer com os créditos pq eu gosto de jogar confete em mim mesmo, e ficou muito bom isso aqui
        """MODESTIA A PARTE"""
        footer_widget = QWidget()
        footer_widget.setStyleSheet("background-color: #676767; border: 0px; margin: 0px; padding: 10px;")
        footer_layout = QHBoxLayout()
        footer_label = QLabel("Desenvolvido por Nise Tech: Soluções em Tecnologia© - 2025")
        footer_label.setStyleSheet("color: white; font-size: 11px;")

        footer_layout.addStretch()
        footer_layout.addWidget(footer_label)
        footer_layout.addStretch()
        footer_layout.setContentsMargins(0, 0, 0, 0)

        footer_widget.setLayout(footer_layout)
        layout_principal.addWidget(footer_widget)

        self.setLayout(layout_principal)

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
    janela.showMaximized()
    sys.exit(app.exec_())
