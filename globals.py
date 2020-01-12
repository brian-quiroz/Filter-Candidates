class Globals:
    def __init__(self):
        self.__regions = ['Amazonas', 'Ancash', 'Apurimac', 'Arequipa',
        'Ayacucho', 'Cajamarca', 'Callao', 'Cusco', 'Huancavelica',
        'Huanuco', 'Ica', 'Junin', 'La Libertad', 'Lambayeque',
        'Lima Provincias', 'Loreto', 'Madre de Dios', 'Moquegua',
        'Pasco', 'Piura', 'Puno', 'San Martin', 'Tacna', 'Tumbes',
        'Ucayali', 'Lima+Exterior']
        self.__parties = ['Alianza para el Progreso', 'Peru Patria Segura', 'Podemos Peru',
        'Peru Libre', 'Fuerza Popular', 'Union por el Peru', 'Frepap', 'Democracia Directa',
        'Frente Amplio', 'Todos por el Peru', 'Contigo', 'PPC', 'Renacimiento Unido',
        'Peru Nacion', 'Juntos por el Peru', 'Apra', 'Avanza Pais', 'Vamos Peru',
        'Somos Peru', 'Partido Morado', 'Accion Popular', 'Solidaridad Nacional']
        self.__studies = ['Uni-Concluido', 'Egresado', 'Bachiller', 'Titulado',
        'Posgrado-Inconcluso', 'Posgrado']
        self.__articleData = []
        self.__history = []
    def get_regions(self):
        return self.__regions
    def get_parties(self):
        return self.__parties
    def get_studies(self):
        return self.__studies
    def get_articleData(self):
        return self.__articleData
    def append_to_articleData(self, val):
        self.__articleData.append(val)
    def reset_articleData(self):
        self.__articleData = []
    def get_history(self):
        return self.__history
    def append_to_history(self, val):
        self.__history = [x for x in self.__history if x[0] != val[0]]
        self.__history.append(val)
    def del_from_history(self, ind):
        del self.__history[ind]

g = Globals()
