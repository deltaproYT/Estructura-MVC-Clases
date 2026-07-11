from views.GUI_Marca import Visual_Marca
from views.GUI_Categoria import Visual_Categoria
from views.GUI_Linea import Visual_Linea
from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QWidget
import sys
from datetime import datetime


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Visual_Marca = None
        self.Visual_Linea = None
        self.Visual_Categoria = None
        self.setWindowTitle('Sistema de Gestión Tecnored')
        self.setGeometry(300, 200, 500, 350)


        # Widget base
        self.Widget_Base = QWidget()
        self.setCentralWidget(self.Widget_Base)

        # Layout horizontal (lado izq: Layout vertical para los botones; Lado der: Imagen de la empresa "Tecnored" junto con mensaje de bienvenida)
        self.Layout_Principal = QHBoxLayout()
        self.Widget_Base.setLayout(self.Layout_Principal)

        # Layout Vertical (Botones de seleccion)
        self.Layout_Botones = QVBoxLayout()
        self.Layout_Principal.addLayout(self.Layout_Botones)

        # Imagen de Portada inicial de la app
        self.Imagen = QWidget()
        self.Layout_Principal.addWidget(self.Imagen)

        # Botones (Boton_Marca: Boton de interfaz de marca; Boton_Categoria: Boton de interfaz de categoria; Boton_Linea: Boton de interfaz de linea)
        self.Boton_Marca = QPushButton('Marca')
        self.Boton_Marca.clicked.connect(self._accion_boton_marca)
        self.Layout_Botones.addWidget(self.Boton_Marca)
        self.Boton_Categoria = QPushButton('Categoria')
        self.Boton_Categoria.clicked.connect(self._accion_boton_categoria)
        self.Layout_Botones.addWidget(self.Boton_Categoria)
        self.Boton_Linea = QPushButton('Linea')
        self.Boton_Linea.clicked.connect(self._accion_boton_linea)
        self.Layout_Botones.addWidget(self.Boton_Linea)

    def _accion_boton_marca(self):
        self.Visual_Marca = Visual_Marca()
        self.Visual_Marca.show()
        self.close()

    def _accion_boton_linea(self):
        self.Visual_Linea = Visual_Linea()
        self.Visual_Linea.show()
        self.close()

    def _accion_boton_categoria(self):
        self.Visual_Categoria = Visual_Categoria()
        self.Visual_Categoria.show()
        self.close()


    @staticmethod
    def iniciar_interfaz_principal():
        try:
            print(f'[{datetime.now()}]// Programa Iniciado')
            app = QApplication(sys.argv)
            ventana_principal = Main()
            ventana_principal.show()
            app.exec()
        except Exception as e:
            print(f'[{datetime.now()}]// ERROR:{e}')

if __name__ == "__main__":
    Main.iniciar_interfaz_principal()


