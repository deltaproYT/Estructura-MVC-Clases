from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal 
from controllers.Controller_Linea import Controlador_Linea
from datetime import datetime
import sys

class Ventana_Datos(QDialog):
    fin_guardado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 200, 500, 400)
        self.controlador_linea = Controlador_Linea()
        self.fl_status = True

    def _Ventana_Agregar(self):
        self.setWindowTitle('Agregar Dato')
        self.Layout_Agregar = QVBoxLayout(self)
        self.inputs = {}
        for campo in self.controlador_linea.Model_Linea.SCHEMA:
            
            if not campo ["editable"]:
                continue

            label = QLabel(f"Ingrese {campo['campo']}")
            linea = QLineEdit()

            self.inputs[campo["campo"]] = linea
            self.Layout_Agregar.addWidget(label)
            self.Layout_Agregar.addWidget(linea)

        self.Layout_Botones = QHBoxLayout()
        self.Layout_Agregar.addLayout(self.Layout_Botones)
        botones = {
            'Cerrar': self.close(), 
            'Guardar': self._Guardar}
        for btn, act in botones.items():
            self.btn = QPushButton(f'{btn}')
            self.btn.clicked.connect(act)
            self.Layout_Botones.addWidget(self.btn)

        self.fl_status = False

    def _Guardar(self):
        try:
            if any(not widget.text() for widget in self.inputs.values()):
                Advertencia_Dato_Incompleto = QMessageBox.question(
                    self,
                    "¡AVERTENCIA!: Informacion Incompleta",
                    "Hay un Campo Vacio\n¿Desea Subir los datos?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                if Advertencia_Dato_Incompleto == QMessageBox.StandardButton.No:
                    return
            
            datos = {
                nombre: widget.text() 
                for nombre, widget in self.inputs.items()
            }

            self.controlador_linea._Guardar_Datos(**datos)

            QMessageBox.information(
                self,
                "Correcto",
                "Los datos fueron guardados."
            )
            print(f'[{datetime.now()}]// Datos Guardados Correctamente')
            self.fin_guardado.emit()
            self.accept()
        except Exception as e:
            print(f'[{datetime.now()}]// ERROR: {e}')

    def iniciar_agg_v(self):
        if self.fl_status:
            self._Ventana_Agregar()
        for widget in self.inputs.values():
            widget.clear()
        self.exec()
