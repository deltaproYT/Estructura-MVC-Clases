from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal 
from controllers.Controller_Linea import Controlador_Linea
from utils.excepciones import InvalidData
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

            texto = campo.get(
                'descripcion',
                f"Ingrese {campo['campo']}"
                )
            label = QLabel(texto)
            widget = QLineEdit()

            self.inputs[campo["campo"]] = widget
            self.Layout_Agregar.addWidget(label)
            self.Layout_Agregar.addWidget(widget)

        self.Layout_Botones = QHBoxLayout()
        self.Layout_Agregar.addLayout(self.Layout_Botones)
        botones = {
            'Cerrar': self.close, 
            'Guardar': self._Guardar}
        for texto, accion in botones.items():
            boton = QPushButton(texto)
            boton.clicked.connect(accion)
            self.Layout_Botones.addWidget(boton)

        self.fl_status = False

    def _Guardar(self):
        try:
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
            print(f'Datos Guardados Correctamente')
            self.fin_guardado.emit()
            self.accept()

        except InvalidData as e:
            QMessageBox.warning(
                self,
                'Datos Invalidos',
                str(e)
            )

        except Exception as e:
            print(f'// ERROR: {e}')

    def _Crear_Widget(self, campo):
        return QLineEdit()

    def iniciar_agg_v(self):
        if self.fl_status:
            self._Ventana_Agregar()
        for widget in self.inputs.values():
            widget.clear()
        self.exec()
