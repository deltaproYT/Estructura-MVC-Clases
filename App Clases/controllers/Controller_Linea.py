from models.Model_Linea import Model_Linea

import sys
from datetime import datetime

class Controlador_Linea():
    def __init__(self):
        self.Model_Linea = Model_Linea()

    def Guardar_Datos(self, nombre, estado):
        self.Model_Linea.nombre = nombre
        self.Model_Linea.estado = estado