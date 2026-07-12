from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from views.Configuracion_Datos_Linea import Ventana_Datos
from controllers.Controller_Linea import Controlador_Linea
from datetime import datetime


class Visual_Linea(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión Tecnored - Linea")
        self.setGeometry(200, 100, 700, 500)
        self.ventana_datos = Ventana_Datos()
        self.controlador_linea = Controlador_Linea()
        self._Configuracion_GUI()
        self.ventana_datos.fin_guardado.connect(self._cargar_tabla)


    def _Configuracion_GUI(self):
        # Widget Base
        self.Widget_Base = QWidget()
        self.setCentralWidget(self.Widget_Base)

        # Layout Base Vertical (Arriba: QLineEdit con informacion alterna sobre lo subido; Abajo: QHBoxLayout con la interfaz principal)
        self.Layout_Base = QVBoxLayout()
        self.Widget_Base.setLayout(self.Layout_Base)

        # QLineEdit
        self.Informacion_Xtra = QLabel()
        self.Informacion_Xtra.setText('Escoja un Item Para ver datos extra')
        self.Layout_Base.addWidget(self.Informacion_Xtra)

        # Layout Botones y Tabla (Izq: QVBoxLayout para poner los botones; Der: QTableView para leer los archivos)
        self.Layout_Interfaz = QHBoxLayout()
        self.Layout_Base.addLayout(self.Layout_Interfaz)

        # Layout Botones (Layout para añadir las 4 funciones de los botones: Agregar - Editar - Eliminar - Volver)
        self.Layout_Botones = QVBoxLayout()
        self.Layout_Interfaz.addLayout(self.Layout_Botones)

        # Lista de datos (Lista con los datos que lea del archivo .txt o de la base de datos en un futuro)
        self.Lista_Datos = QTableView()
        self.Modelo_Lista_Datos = QStandardItemModel()
        self.Lista_Datos.setModel(self.Modelo_Lista_Datos)
        self._cargar_tabla()
        self.Layout_Interfaz.addWidget(self.Lista_Datos)

        # Botones (Los botones con las funciones: Agregar - Editar - Eliminar - Volver)
        self.Agregar_Btn = QPushButton('Agregar')
        self.Agregar_Btn.clicked.connect(self._Agregar_Dato)
        self.Layout_Botones.addWidget(self.Agregar_Btn)
        self.Editar_Btn = QPushButton('Editar')
        self.Editar_Btn.clicked.connect(lambda: print('Boton Editar'))
        self.Layout_Botones.addWidget(self.Editar_Btn)
        self.Eliminar_Btn = QPushButton('Eliminar')
        self.Eliminar_Btn.clicked.connect(lambda: print('Boton Eliminar'))
        self.Layout_Botones.addWidget(self.Eliminar_Btn)
        self.Volver_Btn = QPushButton('Volver')
        self.Volver_Btn.clicked.connect(lambda: print('Boton Volver'))
        self.Layout_Botones.addWidget(self.Volver_Btn)

    def _cargar_tabla(self):
        datos = self.Obtener_Datos()
        self.Modelo_Lista_Datos.clear()
        self.Modelo_Lista_Datos.setHorizontalHeaderLabels([
            "ID_Marca",
            "Nombre",
            "Estado"
        ])
        self.Lista_Datos.verticalHeader().setVisible(False)
        
        if datos:
            for dato in datos:
                self.Modelo_Lista_Datos.appendRow([
                    QStandardItem(dato['ID_Linea']),
                    QStandardItem(dato['Nombre']),
                    QStandardItem(dato['Estado'])
                ])

    def Obtener_Datos(self):
        return self.controlador_linea._Cargar_JSON()


    def _Agregar_Dato(self):
        try:
            print(f'[{datetime.now()}]// Agregando Dato Nuevo')
            self.ventana_datos.iniciar()
            print(f'[{datetime.now()}]// Ventana de Agregar Texto Abierta Correctamente')
        except Exception as e:
            print(f'[{datetime.now()}// ERROR: {e}]')


if __name__ == '__main__': #Pruebas
    pass
