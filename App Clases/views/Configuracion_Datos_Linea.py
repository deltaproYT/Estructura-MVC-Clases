from PyQt6.QtWidgets import *
from controllers.Controller_Linea import Controlador_Linea
from datetime import datetime

import sys

class Ventana_Datos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(450, 200, 500, 400)
        self.Widget_Base = QWidget()
        self.controlador_linea = Controlador_Linea()
        self.setCentralWidget(self.Widget_Base)
        self.fl_status = True

    def _Ventana_Agregar(self):
        self.setWindowTitle('Agregar Dato')
        self.Layout_Agregar = QVBoxLayout()
        self.Widget_Base.setLayout(self.Layout_Agregar)
        self.Label_Nombre = QLabel('Por favor, Ingrese el nombre')
        self.Linea_Nombre = QLineEdit()
        self.Label_Estado = QLabel('Por favor, Ingrese el estado')
        self.Linea_Estado = QLineEdit()
        widgets = (self.Label_Nombre, self.Linea_Nombre, self.Label_Estado, self.Linea_Estado)
        for wgt in widgets:
            self.Layout_Agregar.addWidget(wgt)
        self.Layout_Botones = QHBoxLayout()
        self.Layout_Agregar.addLayout(self.Layout_Botones)
        botones = {'cerrar_btn': lambda: self.close(), 'guardar_datos': lambda: self._Guardar(nombre=self.Linea_Nombre.text(), estado=self.Linea_Estado.text())}
        for btn, act in botones.items():
            self.btn = QPushButton(f'{btn}')
            self.btn.clicked.connect(act)
            self.Layout_Botones.addWidget(self.btn)

        self.fl_status = False

    def _Guardar(self, nombre, estado):
        try:
            self.controlador_linea.Guardar_Datos(nombre= nombre, estado= estado)
            print(f'[{datetime.now()}]// Datos Guardados Correctamente')
        except Exception as e:
            print(f'[{datetime.now()}]// ERROR: {e}')

    def iniciar(self):
        if self.fl_status:
            self._Ventana_Agregar()
        self.Linea_Nombre.setText('')
        self.Linea_Estado.setText('')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana_Datos()
    ventana.show()
    sys.exit(app.exec())