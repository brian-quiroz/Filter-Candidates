import json
import random

class Globals:
    def __init__(self):
        with open('originalCandidates.json') as json_file:
            self.__json_data = json.load(json_file)
            json_file.close()
        random.shuffle(self.__json_data)
        with open('scrapedCandidates.json') as json_file:
            self.__scraped_data = json.load(json_file)
            json_file.close()
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
        self.__studies = ['Secundaria', 'Uni-Concluido', 'Tecnico', 'Egresado', 'Bachiller', 'Titulado',
        'Posgrado-Inconcluso', 'Posgrado']
        self.__articleData = []
        self.__history = []
        self.__amount = 0
        self.__page = 1
        self.__saved = []
    def get_json_data(self):
        return self.__json_data
    def get_scraped_data(self):
        return self.__scraped_data
    def get_regions(self):
        return self.__regions
    def get_value_from_regions(self, ind):
        return self.__regions[ind]
    def get_parties(self):
        return self.__parties
    def get_value_from_parties(self, ind):
        return self.__parties[ind]
    def get_studies(self):
        return self.__studies
    def get_value_from_studies(self, ind):
        return self.__studies[ind]
    def get_articleData(self):
        return self.__articleData
    def get_length_of_articleData(self):
        return len(self.__articleData)
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
    def get_tag_text(self, action, val):
        if (action == "regions"):
            return "Región: " + self.__regions[int(val) - 1]
        elif (action == "partiesIncl"):
            return "Incluir: " + ", ".join(map(lambda x: self.__parties[int(x) - 1], val))
        elif (action == "partiesExcl"):
            return "Excluir: " + ", ".join(map(lambda x: self.__parties[int(x) - 1], val))
        elif (action == "experience"):
            return "Con Exp. Pol."
        elif (action == "studies"):
            return "Estudios >= " + self.__studies[int(val) - 1]
        elif (action == "sentence"):
            return "Sin Sentencias"
        elif (action == "ageLower"):
            return "Menores que " + str(val)
        elif (action == "ageUpper"):
            return "Mayores que " + str(val)
        elif (action == "gender"):
            return "Género: " + val
        elif (action == "candidate"):
            return "Nombre: " + val
        else:
            return "Error!"
    def get_amount(self):
        return self.__amount
    def set_amount(self, amount):
        self.__amount = amount
    def get_page(self):
        return self.__page
    def set_page(self, page):
        self.__page = page
    def get_saved(self):
        return self.__saved
    def append_to_saved(self, val):
        self.__saved.append(val)
    def del_from_saved(self, ind):
        del self.__saved[ind]

g = Globals()
