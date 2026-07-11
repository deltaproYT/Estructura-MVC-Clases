class Marca:
    def __init__(self, ID_Marca, nombre, estado):
        self.ID_Marca = 0
        self.nombre = nombre
        self.estado = estado

    @property
    def indexacion_progresiva(self, indices):
        for idx in indices:
            pass