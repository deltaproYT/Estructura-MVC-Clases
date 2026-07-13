class Model_Linea:
    """ DOCUMENTACION
    i_2 SCHEMA
    i_4 Cada elemento del SCHEMA describe un campo de la entidad.

    i_2 Propiedades disponibles:
    i_1 - "campo":
        i_4 Nombre interno del campo.

    i_1 - "tipo":
        i_4 Tipo de dato esperado (str, int, float, bool, etc.).

    i_1 - "unico":
        i_4 Indica si el valor debe ser único dentro de la entidad.

    i_1 - "requerido":
        i_4 True  -> El campo debe contener un valor.
        i_4 False -> El campo puede quedar vacío.

    i_1 - "opciones":
        i_4 Lista de valores permitidos.
        i_4 Si es None o una lista vacía, el campo acepta cualquier valor válido.

    i_1 - "min":
        i_4 Longitud mínima permitida (o valor mínimo para tipos numéricos).

    i_1 - "max":
        i_4 Longitud máxima permitida (o valor máximo para tipos numéricos).

    i_1 - "default":
        i_4 Valor asignado cuando el usuario no proporciona uno.

    i_1 - "editable":
        i_4 Indica si el usuario puede modificar este campo desde la aplicación.

    i_1 - "pk":
        i_4 Indica si el campo es una Primary Key

    i_1 - "generador":
        i_4 Nombre del generador automático que utilizará el controlador.
        i_4 Si es None, el campo no se genera automáticamente.

    i_1 - "descripcion":
        i_4 Breve explicación del propósito del campo.

    """

    SCHEMA = [
        {"campo": "ID_Linea",
        "tipo": int,
        "editable": False, 
        "unico": True,
        "requerido": True,
        "generador": "indice",
        "descripcion": "Primary Key de el dataset"},

        {"campo": "Nombre",
        "requerido": True,
        "editable": True, 
        "tipo": str,
        },

        {"campo": "Estado", 
        "editable": True, 
        "tipo": str}
    ]

    FORMULARIO = {}

    def __init__(self):
        self.ID_Linea = ""
        self.Nombre = ""
        self.Estado = ""
