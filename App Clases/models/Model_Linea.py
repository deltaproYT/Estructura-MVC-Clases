class Model_Linea:
    """ DOCUMENTACION
    i_3 SCHEMA
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

    i_3 FORMULARIO
    i_4 Cada elemento de FORMULARIO describe cómo debe construirse
    i_4 la interfaz de edición para un campo del modelo.

    i_1 - "label":
        i_4 Texto descriptivo mostrado al usuario.    

    i_1 - "tipo":
        i_4 Define el tipo de widget que utilizará el campo.
        i_4 Este atributo es obligatorio.
        i_4 "lineedit"     -> QLineEdit()
        i_4 "combobox"     -> QComboBox()
        i_4 "spinbox"      -> QSpinBox()
        i_4 "doublespin"   -> QDoubleSpinBox()
        i_4 "checkbox"     -> QCheckBox()
        i_4 "dateedit"     -> QDateEdit()
        i_4 "timeedit"     -> QTimeEdit()
        i_4 "datetime"     -> QDateTimeEdit()
        i_4 "textedit"     -> QTextEdit()

    i_1 - "placeholder":
        i_4 Texto de ayuda mostrado dentro de widgets 
        i_4 Compatible con widgets que soporten placeholder
        i_4 QLineEdit()
        i_4 QTextEdit()

    i_1 - "items":
        i_4 Lista de opciones disponibles para widgets de seleccion
        i_4 QComboBox()

    i_1 - "visible":
        i_4 Define si el widget será visible dentro del formulario.
        i_4 True  -> Visible.
        i_4 False -> Oculto.

    i_2 Todo campo definido en FORMULARIO debe existir previamente en SCHEMA.
    i_2 Un campo puede existir en SCHEMA sin aparecer en FORMULARIO.
    i_2 Solo FORMULARIO define la apariencia de la interfaz.
    i_2 Toda validación pertenece a SCHEMA.
    """

    SCHEMA = [
        {"campo": "ID_Linea",
        "tipo": int,
        "pk": True,
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

    FORMULARIO = {
        "Nombre" : {
            "tipo": "lineedit",
            "label": "Nombre",
            "placeholder": "Ingrese el nombre"
        },

        "Estado": {
            "tipo": "combobox",
            "label": "Estado",
            "items": ["Activo", "Inactivo"]
        }
    }

    def __init__(self):
        self.ID_Linea = ""
        self.Nombre = ""
        self.Estado = ""
