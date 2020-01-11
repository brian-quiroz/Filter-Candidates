from globals import g

def filterRegions(selected, ind):
    return [x for x in selected if x["Region"] == g.get_regions()[ind - 1].upper()]

def filterPartiesIncl (filt, inds):
    return [x for x in filt if any(map(lambda ind: x["Partido"] == g.get_parties()[ind - 1].upper(), inds))]

def filterPartiesExcl (filt, inds):
    return [x for x in filt if all(map(lambda ind: x["Partido"] != g.get_parties()[ind - 1].upper(), inds))]

def filterExperience(selected):
    return [x for x in selected if x["Experiencia_Pol"] == "Sí"]

def filterStudies(selected, grade):
    return [x for x in selected if "Estudios" in x and g.get_studies().index(x["Estudios"]) >= grade - 1]

def filterSentence(selected):
    return [x for x in selected if x["ConSentencia"] == "Sin Sentencia"]

def filterAgeLower(selected, lower):
    return [x for x in selected if int(x["Edad"]) >= lower]

def filterAgeUpper(selected, upper):
    return [x for x in selected if int(x["Edad"]) <= upper]

def filterGender(selected, gender):
    return [x for x in selected if x["Sexo"] == "Hombre"]

def filterCandidate(selected, name):
    return [x for x in selected if x["Candidato"] == name.upper()]
