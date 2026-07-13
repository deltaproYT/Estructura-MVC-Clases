'''
Pendientes a futuro:
🔲 Validar expresiones regulares (regex)
🔲 Validar correo electrónico
🔲 Validar longitud exacta
🔲 Valores mínimos y máximos para fechas
🔲 Generadores nuevos (uuid, datetime, etc.)
🔲 Hooks (before_save, after_save)
🔲 Relaciones entre modelos
'''

from models.Model_Linea import Model_Linea
from utils.excepciones import InvalidData
from pathlib import Path
import json
from datetime import datetime

class Controlador_Linea():
    def __init__(self):
        self.Model_Linea = Model_Linea()
        self.Ruta_Padre = Path(f'{Path(__file__).parent.parent}/media')
        self.Ruta_Padre.mkdir(parents= True, exist_ok=True)

    def _Guardar_Datos(self, **kwargs):
        generadores = {
            "indice": lambda: str(self._Calcular_Indice())
        }

        for campo in self.Model_Linea.SCHEMA:
            valor = self._Obtener_Valor_Campo(
                campo,
                kwargs,
                generadores
            )

            valor = self._Aplicar_Default(campo, valor)

            valor = self._Convertir_Tipo(campo, valor)

            self._Validar_Campo(campo, valor)

            setattr(
                self.Model_Linea,
                campo["campo"],
                valor
            )

        self._Exportar_Datos(self._Serializar_Modelo())

    def _Exportar_Datos(self, datos):
        ruta = f"{self.Ruta_Padre}/Datos_Linea.json"
        try:
            try:
                with open(ruta, 'r') as f:
                    lista_datos = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                lista_datos = []

            lista_datos.append(datos)
            with open(ruta, "w") as f:
                json.dump(lista_datos, f, indent=4)
            print(f'[{datetime.now()}]// Archivo Guardado Completamente')
        except Exception as e:
            print(f'[{datetime.now()}]// ERROR: {e}')

    def _Calcular_Indice(self):
        try:
            with open(f"{self.Ruta_Padre}/Datos_Linea.json", "r") as f:
                lista_datos = json.load(f)
                return len(lista_datos) + 1
        except (FileNotFoundError, json.JSONDecodeError):
            return 1

    def _Cargar_JSON(self):
        while True:
            try:
                with open(f"{self.Ruta_Padre}/Datos_Linea.json", "r") as f:
                    lista_datos = json.load(f)
                    return lista_datos
            except FileNotFoundError:
                with open(f"{self.Ruta_Padre}/Datos_Linea.json", "a") as f:
                    f.write('')
            except json.JSONDecodeError:
                return

    def _Guarda_JSON(self, lista_datos):
        with open(f"{self.Ruta_Padre}/Datos_Linea.json", "w") as f:
            json.dump(lista_datos,f, indent=4)

    def _Obtener_Valor_Campo(self, campo, kwargs, generadores):
        nombre = campo["campo"]
        generador = campo.get("generador")

        if generador:
            funcion = generadores.get(generador)

            if funcion is None:
                raise InvalidData(
                    f'Generador "{generador}" no registrado'
                )
            return funcion()
        return kwargs.get(nombre)

    def _Serializar_Modelo(self):
        return {
            campo["campo"]: getattr(self.Model_Linea, campo["campo"])for campo in self.Model_Linea.SCHEMA
        }

    def _Convertir_Tipo(self, campo, valor):
        tipo = campo.get('tipo')

        if tipo is None:
            return valor

        try: 
            if valor is None:
                return None
            return tipo(valor)
        except (ValueError, TypeError):
            raise InvalidData(
                f'No se pudo convertir {campo["campo"]} a {tipo.__name__}.'
            )

    def _Obtener_PK(self):
        for campo in self.Model_Linea.SCHEMA:
            if campo.get('pk'):
                return campo["campo"]

    def _Obtener_Datos(self):
        return self._Cargar_JSON()
#i_2 <---- Filtros de Validacion ---->
    def _Validar_Campo(self, campo, valor):
        self._Validar_Requerido(campo, valor)
        self._Validar_Tipo(campo, valor)
        self._Validar_Opciones(campo, valor)
        self._Validar_Min(campo, valor)
        self._Validar_Max(campo, valor)
        self._Validar_Unico(campo, valor)

    def _Validar_Requerido(self, campo, valor):
        if campo.get("requerido") and valor in (None, ""):
            raise InvalidData(
                f'El campo "{campo["campo"]}" es obligatorio.'
            )

    def _Validar_Tipo(self, campo, valor):
        tipo = campo.get("tipo")

        if tipo is None:
            return

        if valor is None:
            return

        if not isinstance(valor, tipo):
            raise InvalidData(
                f'El campo "{campo["campo"]}" debe ser de tipo {tipo.__name__}.'
            )

    def _Aplicar_Default(self, campo , valor):
        if valor in (None, ""):
            return campo.get('default', valor)

        return valor
    
    def _Validar_Opciones(self, campo, valor):
        opciones = campo.get('opciones')

        if not opciones:
            return
        
        if valor not in opciones:
            raise InvalidData(
                    f'El valor "{valor}" no es válido para '
                    f'"{campo["campo"]}". '
                    f'Valores permitidos: {", ".join(map(str, opciones))}.'
            )

    def _Validar_Min(self, campo, valor):
        minimo = campo.get('min')

        if minimo is None:
            return

        if isinstance(valor ,(int, float)):
            if valor < minimo:
                raise InvalidData(
                    f"El campo {campo["campo"]} debe ser mayor o igual a {minimo}"
                )
        elif isinstance(valor, str):
            if len(valor) < minimo:
                raise InvalidData(
                    f"El campo {campo["campo"]} debe tener al menos {minimo} caracteres"
                )

    def _Validar_Max(self, campo, valor):
        maximo = campo.get('max')

        if maximo is None:
            return

        if isinstance(valor ,(int, float)):
            if valor > maximo:
                raise InvalidData(
                    f"El campo {campo['campo']} debe ser menor o igual a {maximo}"
                )
        elif isinstance(valor, str):
            if len(valor) > maximo:
                raise InvalidData(
                    f"El campo {campo['campo']} debe tener como maximo {maximo} caracteres"
                )

    def _Validar_Unico(self, campo, valor, id_actual=None):
        if not campo.get('unico'):
            return

        nombre = campo["campo"]
        pk = self._Obtener_PK()

        if pk is None:
            raise InvalidData(
                f"No existe una Clave Primaria definida en el SCHEMA"
            )

        lista = self._Cargar_JSON() or []

        for registro in lista():

            if id_actual is not None and registro.get(pk) == id_actual:
                if registro.get(nombre) == valor:                    raise InvalidData(                        f'El valor "{valor}" ya existe para el campo "{nombre}".'                    )
                continue

            if registro.get(nombre) == valor:
                raise InvalidData(
                    f"El valor {valor} ya existe para el campo {nombre}."
                )
