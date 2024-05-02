import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTabWidget, QLabel, \
    QFileDialog, QTextEdit, QTableWidget, QComboBox, QTableWidgetItem
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import shutil
import pandas as pd

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Nombres de las pestañas
        tab_names = ["INFO", "GENERADOR QFIELD-URBANO","GENERADOR QFIELD-RURAL"]

        # Estilo de la ventana principal
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #efa229, stop:1 #e8c39e);
            }
            QPushButton {
                background-color: #00B4D8;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e80729;
            }
            #orange_button {
                background-color: #e80729; 
            }
        """)

        # Crear un widget central y un diseño vertical
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)


        # Crear un widget de pestañas
        tab_widget = QTabWidget(self)
        layout.addWidget(tab_widget)

        # Crear pestañas
        for i, tab_name in enumerate(tab_names):
            tab = QWidget(self)
            tab_layout = QVBoxLayout(tab)
            tab_widget.addTab(tab, tab_name)

            if i == 0:
                # Establecer el diseño de la pestaña DESARROLLADOR
                # Espacio para poner la descripción de desarrollo e instrucciones
                carpeta_origen_relative_path = r'..\Img\hustle.png'
                base_directory = os.path.abspath(os.path.dirname(__file__))  # Directorio del script actual
                imagen_path = os.path.abspath(os.path.join(base_directory, carpeta_origen_relative_path))
                imagen_label = QLabel(self)
                imagen = QPixmap(imagen_path)
                imagen_label.setPixmap(imagen)
                tab_layout.addWidget(imagen_label)

            elif i == 1:
                # Establecer el diseño de la pestaña EJECUTOR
                self.create_ejecutor_tab_layout(tab_layout)
            elif i == 2:
                # Establecer el diseño de la tercera pestaña (Base de Datos)
                self.create_third_tab_layout(tab_layout)

            tab.setLayout(tab_layout)
            
    def create_ejecutor_tab_layout(self, tab_layout):
        base_directory = os.path.abspath(os.path.dirname(__file__))  # Directorio del script actual
        button_info = [
            ("1°-Descargar Datos desde Server", "gdb_server_to_project_urbano.bat"),
            ("2°-Depurar los datos Descargados", "depurar_tablas_urbano.bat"),
            ("3°-Desplegar datos en los Directorios", "shp_urbano_to_dir.bat"),
            ("4°-Compilar Qfield Urbano", "compiler_urbano.bat")
        ]

        for button_text, button_filename in button_info:
            button_path = os.path.join(base_directory, "bat", button_filename)
            button = QPushButton(button_text, self)
            button.clicked.connect(lambda _, path=button_path: os.system(f'start {path}'))
            tab_layout.addWidget(button)
            button.setStyleSheet("""
            QPushButton {
                background-color: #00B4D8;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0097B9;
            }
            """)

            if button_text == "4°-Compilar Qfield Urbano":
                button.setStyleSheet("background-color: #FF0100;")
                tab_layout.addWidget(button)

    def create_third_tab_layout(self, tab_layout):
        base_directory = os.path.abspath(os.path.dirname(__file__))  # Directorio del script actual
        button_info = [
            ("1°-Descargar Datos desde Server", "gdb_server_to_project_rural.bat"),
            ("2°-Depurar los datos Descargados", "depurar_tablas_rural.bat"),
            ("3°-Desplegar datos en los Directorios", "shp_rural_to_dir.bat"),
            ("4°-Compilar Qfield Rural", "compiler_rural.bat")
        ]

        for button_text, button_filename in button_info:
            button_path = os.path.join(base_directory, "bat", button_filename)
            button = QPushButton(button_text, self)
            button.clicked.connect(lambda _, path=button_path: os.system(f'start {path}'))
            tab_layout.addWidget(button)
            button.setStyleSheet("""
            QPushButton {
                background-color: #009929;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5ccb5f;
            }
            """)

            if button_text == "4°-Compilar Qfield Rural":
                button.setStyleSheet("background-color: #FF0100;")
                tab_layout.addWidget(button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.setGeometry(100, 100, 500, 600)
    main_window.setWindowTitle('Automatizacion Para Generar Paquetes QFIELD URBANO-RURAL')
    main_window.show()
    sys.exit(app.exec_())
