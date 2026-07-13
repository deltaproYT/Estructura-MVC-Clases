from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, QDate, QDateTime, QTime

from controllers.Controller_Linea import Controlador_Linea
from utils.excepciones import InvalidData
import sys

class Ventana_Datos(QDialog):
    fin_guardado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 200, 500, 400)
        self.controlador_linea = Controlador_Linea()
        self.formulario_creado = True

    def _Ventana_Agregar(self):
        self.setWindowTitle('Agregar Dato')
        self.Layout_Agregar = QVBoxLayout(self)
        self.inputs = {}
        for campo in self.controlador_linea.Model_Linea.SCHEMA:
            
            if not campo ["editable"]:
                continue

            config = self.controlador_linea.Model_Linea.FORMULARIO.get(campo["campo"])

            if config is None:
                raise InvalidData(
                    f'No existe configuración para "{campo["campo"]}".'
                )

            label = QLabel(
                config.get(
                    "label",
                    campo["campo"]
                )
            )

            widget = self._Crear_Widget(campo)

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

        self.formulario_creado = False

    def _Guardar(self):
        try:
            datos = {
                nombre: self._Obtener_Valor_Widget(widget)
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
        nombre = campo["campo"]
        config = self.controlador_linea.Model_Linea.FORMULARIO.get(nombre)

        if config is None:
            raise InvalidData(
                f'No existe configuración de formulario para "{nombre}".'
            )
        tipo = config.get('tipo')
        
        constructores = {
            "lineedit": self._Crear_LineEdit,
            "combobox": self._Crear_ComboBox,
            "spinbox": self._Crear_SpinBox,
            "doublespin": self._Crear_DoubleSpin,
            "checkbox": self._Crear_CheckBox,
            "dateedit": self._Crear_DateEdit,
            "timeedit": self._Crear_TimeEdit,
            "datetime": self._Crear_DateTimeEdit,
            "textedit": self._Crear_TextEdit
        }

        constructor = constructores.get(tipo)

        if constructor is None:
            raise InvalidData(
                f'Tipo de widget "{tipo}" no soportado.'
            )

        return constructor(config)

    def _Crear_LineEdit(self, config):
        widget = QLineEdit()

        placeholder = config.get('placeholder')
        if placeholder:
            widget.setPlaceholderText(placeholder)

        return widget

    def _Crear_ComboBox(self, config):
        widget = QComboBox()

        widget.addItems(config.get('items', []))

        return widget

    def _Crear_SpinBox(self, config):
        widget = QSpinBox()

        widget.setMinimum(config.get("min", 0))
        widget.setMaximum(config.get("max", 999999))
        widget.setSingleStep(config.get("step", 1))

        return widget

    def _Crear_DoubleSpin(self, config):
        widget = QDoubleSpinBox()

        widget.setMinimum(config.get("min", 0))
        widget.setMaximum(config.get("max", 999999))
        widget.setSingleStep(config.get("step", 1))

        return widget

    def _Crear_CheckBox(self, config):
        widget = QCheckBox()

        return widget

    def _Crear_DateEdit(self, config):
        widget = QDateEdit()

        widget.setCalendarPopup(True)

        return widget

    def _Crear_TimeEdit(self, config):
        widget = QTimeEdit()

        return widget

    def _Crear_DateTimeEdit(self, config):
        widget = QDateTimeEdit()

        widget.setCalendarPopup(True)
        return widget

    def _Crear_TextEdit(self, config):
        widget = QTextEdit()

        placeholder = config.get('placeholder')
        if placeholder:
            widget.setPlaceholderText(placeholder)

        return widget

    def _Obtener_Valor_Widget(self, widget):
        lectores = {
            QLineEdit: lambda w: w.text(),
            QTextEdit: lambda w: w.toPlainText(),
            QComboBox: lambda w: w.currentText(),
            QSpinBox: lambda w: w.value(),
            QDoubleSpinBox: lambda w: w.value(),
            QCheckBox: lambda w: w.isChecked(),
            QDateEdit: lambda w: w.date().toPyDate(),
            QTimeEdit: lambda w: w.time().toPyTime(),
            QDateTimeEdit: lambda w: w.dateTime().toPyDateTime(),
        }

        for tipo, lector in lectores.items():
            if isinstance(widget, tipo):
                return lector(widget)
        raise InvalidData(
            "Tipo de Widget no soportado"
        )

    def _Asignar_Valor_Widget(self, widget, valor):
        escritores = {
            QLineEdit: lambda w, v: w.setText(v),
            QTextEdit: lambda w, v: w.setPlainText(v),
            QComboBox: lambda w, v: w.setCurrentText(v),
            QSpinBox: lambda w, v: w.setValue(v),
            QDoubleSpinBox: lambda w, v: w.setValue(v),
            QCheckBox: lambda w, v: w.setChecked(v),
            QDateEdit: lambda w, v: w.setDate(v),
            QTimeEdit: lambda w, v: w.setTime(v),
            QDateTimeEdit: lambda w, v: w.setDateTime(v),
        }

        for tipo, escritor in escritores.items():
            if isinstance(widget, tipo):
                escritor(widget, valor)
                return
        
        raise InvalidData(
                "Tipo de widget no soportado."
        )

    def _Limpiar_Widget(self, widget):
        limpiadores = {
            QLineEdit: lambda w: w.clear(),
            QTextEdit: lambda w: w.clear(),
            QComboBox: lambda w: w.setCurrentIndex(0),
            QSpinBox: lambda w: w.setValue(w.minimum()),
            QDoubleSpinBox: lambda w: w.setValue(w.minimum()),
            QCheckBox: lambda w: w.setChecked(False),
            QDateEdit: lambda w: w.setDate(QDate.currentDate()),
            QTimeEdit: lambda w: w.setTime(QTime.currentTime()),
            QDateTimeEdit: lambda w: w.setDateTime(QDateTime.currentDateTime()),
        }

        for tipo,limpiar in limpiadores.items():
            if isinstance(widget, tipo):
                limpiar(widget)
                return

        raise InvalidData(
            "Tipo de widget no soportado."
        )

    def iniciar_agg_v(self):
        if self.formulario_creado:
            self._Ventana_Agregar()
        for widget in self.inputs.values():
            self._Limpiar_Widget(widget)
        self.exec()
