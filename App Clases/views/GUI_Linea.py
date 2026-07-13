from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt, pyqtSignal
from views.Configuracion_Datos_Linea import Ventana_Datos
from controllers.Controller_Linea import Controlador_Linea
from datetime import datetime


class Visual_Linea(QMainWindow):

    def __init__(self):
        super().__init__()
        self.Edit_Mode = True
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
        if self.Edit_Mode:
            self.Lista_Datos.clicked.connect(self._toggle_click)

        # Botones (Los botones con las funciones: Agregar - Editar - Eliminar - Volver)
        self.Agregar_Btn = QPushButton('Agregar')
        self.Agregar_Btn.clicked.connect(self._Agregar_Dato)
        self.Layout_Botones.addWidget(self.Agregar_Btn)
        self.Editar_Btn = QPushButton('Editar')
        self.Editar_Btn.clicked.connect(self._Toggle_Edit_Mode)
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
                ID_Marca = QStandardItem(dato['ID_Linea'])
                ID_Marca.setEditable(False)
                Nombre = QStandardItem(dato['Nombre'])
                Estado = QStandardItem(dato['Estado'])
                self.Modelo_Lista_Datos.appendRow([
                    ID_Marca,
                    Nombre,
                    Estado
                ])
        self.Lista_Datos.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def Obtener_Datos(self):
        return self.controlador_linea._Cargar_JSON()

    def _Agregar_Dato(self):
        try:
            print(f'[{datetime.now()}]// Agregando Dato Nuevo')
            self.ventana_datos.iniciar_agg_v()
            print(f'[{datetime.now()}]// Ventana de Agregar Texto Abierta Correctamente')
        except Exception as e:
            print(f'[{datetime.now()}// ERROR: {e}]')

    def _Guardar_Cambios(self):
        datos = []
        for fila in range(self.Modelo_Lista_Datos.rowCount()):
            datos.append({
                "ID_Linea": self.Modelo_Lista_Datos.item(fila, 0).text(),
                "Nombre": self.Modelo_Lista_Datos.item(fila, 1).text(),
                "Estado": self.Modelo_Lista_Datos.item(fila, 2).text()
            })
        self.controlador_linea._Guarda_JSON(lista_datos=datos)

    def _Toggle_Edit_Mode(self):
        if self.Edit_Mode: # Modo Edición Activado - True
            self.Lista_Datos.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
            self.Lista_Datos.clicked.connect(lambda: None)
            self.Informacion_Xtra.setText('🔴 MODO EDICION ACTIVO 🔴')
        else: # Modo Edición Desactivado - False
            self.Lista_Datos.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.Informacion_Xtra.setText('Escoja un Item Para ver datos extra')
            self._Guardar_Cambios()
        self.Edit_Mode = not self.Edit_Mode

    def _toggle_click(self, indice):
        if  not self.Edit_Mode: 
            return

        if not indice.isValid():
            return

        header = self.Modelo_Lista_Datos.headerData(
            indice.column(),
            Qt.Orientation.Horizontal
        )

        self.Informacion_Xtra.setText(f"{header} = {indice.data()}")
