from models.Model_Linea import Model_Linea
from pathlib import Path
import json
from datetime import datetime

class Controlador_Linea():
    def __init__(self):
        self.Model_Linea = Model_Linea()
        self.Ruta_Padre = Path(f'{Path(__file__).parent.parent}/media')
        self.Ruta_Padre.mkdir(parents= True, exist_ok=True)

    def Guardar_Datos(self, nombre, estado):
        if nombre:
            self.Model_Linea.nombre = nombre
        else:
            self.Model_Linea.nombre = None
        if estado:
            self.Model_Linea.estado = estado
        else:
            self.Model_Linea.estado = None

        indice = self._Calcular_Indice()
        self.datos = {"ID_Linea": str(indice), "Nombre": self.Model_Linea.nombre, "Estado": self.Model_Linea.estado}
        self._Exportar_Datos()


    def _Exportar_Datos(self):
        ruta = f"{self.Ruta_Padre}/Datos_Linea.json"
        try:
            try:
                with open(ruta, 'r') as f:
                    list_datos = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                list_datos = []

            list_datos.append(self.datos)
            with open(ruta, "w") as f:
                json.dump(list_datos, f, indent=4)
            print(f'[{datetime.now()}]// Archivo Guardado Completamente')
        except Exception as e:
            print(f'[{datetime.now()}]// ERROR: {e}')

    def _Leer_Datos(self):
        pass

    def _Calcular_Indice(self):
        try:
            with open(f"{self.Ruta_Padre}/Datos_Linea.json", "r") as f:
                Lista_Datos = json.load(f)
                return len(Lista_Datos) + 1
        except (FileNotFoundError, json.JSONDecodeError):
            return 1
    
    def _Cargar_JSON(self):
        while True:
            try:
                with open(f"{self.Ruta_Padre}/Datos_Linea.json", "r") as f:
                    Lista_Datos = json.load(f)
                    return Lista_Datos
            except FileNotFoundError:
                with open(f"{self.Ruta_Padre}/Datos_Linea.json", "a") as f:
                    f.write('')
            except json.JSONDecodeError:
                return