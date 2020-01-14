# importing packages
import sys
import numpy as np
import json
import requests
from bs4 import BeautifulSoup
from filters import *
from globals import g

def run2(page):
    g.reset_articleData()

    selected = rerun(g.get_json_data())
    g.set_amount(len(selected))
    print("Selected " + str(len(selected)))

    people = [x["Candidato"] for x in selected]
    print("Results" + str(0 + 5*(page - 1) + 1) + "through" + str(5 + 5*(page -1)))
    sample = people[0 + 5*(page - 1):5 + 5*(page - 1)]

    for i in range(0, len(sample)):
        scrape(sample[i].lower())
    print("Article data: " + str(len(g.get_articleData())))
    return g.get_articleData()

def run():
    with open('candidatos.json') as json_file:
        data = json.load(json_file)
        json_file.close()

    selected = [x for x in data]
    opt1 = 0
    print("Bienvenido/a!")
    while(opt1 != 6):
        print("\nQué deseas hacer?:")
        print("1) Añadir filtros")
        print("2) Remover filtros")
        print("3) Ver filtros")
        print("4) Ver cantidad de candidatos seleccionados")
        print("5) Ver candidatos")
        print("6) Salir")
        opt1 = int(input("Opción: "))

        if (opt1 == 1):
            print("\nElige un filtro:")
            print("1) Región")
            print("2) Partido")
            print("3) Experiencia Política")
            print("4) Estudios")
            print("5) Sin Sentencias")
            print("6) Edad")
            print("7) Género")
            print("8) Nombre")
            opt2 = int(input("Opción: "))

            oldLen = len(selected)
            if (opt2 == 1):
                selected = selectRegions(selected)

            elif (opt2 == 2):
                selected = selectParties(selected)

            elif (opt2 == 3):
                selected = selectExperience(selected)

            elif (opt2 == 4):
                selected = selectStudies(selected)

            elif (opt2 == 5):
                selected = selectSentence(selected)

            elif (opt2 == 6):
                selected = selectAge(selected)

            elif (opt2 == 7):
                selected = selectGender(selected)

            elif (opt2 == 8):
                selected = selectCandidate(select)

            print(str(len(selected)) + " de "  + str(oldLen) + " candidatos seleccionados!")

        elif (opt1 == 2):
            printFilters()
            toDel = int(input("Opción: ")) - 1
            g.del_from_history(toDel)
            selected = rerun(data)

        elif (opt1 == 3):
            printFilters()

        elif (opt1 == 4):
            print(str(len(selected)) + " candidatos seleccionados.")

        elif (opt1 == 5):
            people = [x["Candidato"] for x in selected]
            sample = people[:10]
            print(len(selected))
            for i in range(0, len(sample)):
                scrape(sample[i].lower())
            printData()

def selectRegions(selected):
    print("\nSelecciona una región:")
    for i in range(0, len(g.get_regions())):
        print(str(i + 1) + ") " + g.get_value_from_regions(i))
    opt3 = int(input("Opción: "))
    g.append_to_history(["regions", lambda selected, ind: filterRegions(selected, ind), opt3])
    return filterRegions(selected, opt3)

def selectParties(selected):
    print("\nElegir candidato que:")
    print("1) Pertenezcan al/los partido(s)")
    print("2) NO pertenezcan al partido(s)")
    opt3 = int(input("Opción: "))

    print("\nElegir partido(s)")
    for i in range(0, len(g.get_parties())):
        print(str(i + 1) + ") " + g.get_value_from_parties(i))

    if (opt3 == 1):
        filt = selected
        opt4 = list(map(lambda x: int(x), input("Partido(s) deseado(s): ").split()))
        g.append_to_history(["partiesIncl", lambda selected, inds: filterPartiesIncl(selected, inds), opt4])
        return filterPartiesIncl(filt, opt4)
    elif (opt3 == 2):
        filt = selected
        opt4 = list(map(lambda x: int(x), input("Partido(s) NO deseado(s): ").split()))
        g.append_to_history(["partiesExcl", lambda selected, inds: filterPartiesExcl(selected, inds), opt4])
        return filterPartiesExcl(filt, opt4)
    else:
        return selected

def selectExperience(selected):
    g.append_to_history(["experience", lambda selected: filterExperience(selected), ""])
    return filterExperience(selected)

def selectStudies(selected):
    print("\nElegir candidatos cuyo mínimo nivel de estudio:")
    for i in range(0, len(g.get_studies())):
        print(str(i + 1) + ") " + g.get_value_from_studies(i))
    opt3 = int(input("Opción: "))
    g.append_to_history(["studies", lambda selected, level: filterStudies(selected, level), opt3])
    return filterStudies(selected, opt3)

def selectSentence(selected):
    g.append_to_history(["sentence", lambda selected: selectSentence(selected), ""])
    return filterSentence(selected)

def selectAge(selected):
    print("\nElegir candidatos con:")
    print("1) Límite inferior")
    print("2) Límite superior")
    opt3 = int(input("Opción: "))
    if (opt3 == 1):
        opt4 = int(input("Límite inferior: "))
        g.append_to_history(["ageLower", lambda selected, lower: filterAgeLower(selected, lower), opt4])
        return filterAgeLower(selected, opt4)
    elif (opt3 == 2):
        opt4 = int(input("Límite superior: "))
        g.append_to_history(["ageUpper", lambda selected, upper: filterAgeUpper(selected, upper), opt4])
        return filterAgeUpper(selected, opt4)
    else:
        return selected

def selectGender(selected):
    print("\nElegir candidatos cuyo género sea:")
    print("1) Hombre")
    print("2) Mujer")
    opt3 = int(input("Opción: "))
    if (opt3 == 1):
        g.append_to_history(["gender", lambda selected, gender: filterGender(selected, gender), "Hombre"])
        return filterGender(selected, "Hombre")
    elif (opt3 == 2):
        g.append_to_history(["gender", lambda selected, gender: filterGender(selected, gender), "Mujer"])
        return filterGender(selected, "Mujer")
    else:
        return selected

def selectCandidate(selected):
    name = input("Escribe el nombre del candidato: ")
    g.append_to_history(["candidate", lambda selected, candidate: filterCandidate(selected, candidate), name])
    return filterCandidate(selected, name)

def printFilters():
    print("\nFiltros:")
    i = 1
    for action in g.get_history():
        tag = action[0]
        if tag == "regions":
            print(str(i) + ") Solo candidatos de la región " + g.get_value_from_regions(action[2] - 1))
        elif tag == "partiesIncl":
            partiesIncluded = ", ".join(map(lambda x: g.get_value_from_parties(x - 1), action[2]))
            print(str(i) + ") Solo candidatos que sean de el/los partido(s) " + partiesIncluded)
        elif tag == "partiesExcl":
            partiesExcluded = ", ".join(map(lambda x: g.get_value_from_parties(x - 1), action[2]))
            print(str(i) + ") Solo candidatos que no sean de el/los partido(s) " + partiesExcluded)
        elif tag == "experience":
            print(str(i) + ") Solo candidatos con experiencia política")
        elif tag == "studies":
            print(str(i) + ") Solo candidatos con estudios superiores o iguales a " + g.get_value_from_studies(action[2] - 1))
        elif tag == "sentence":
            print(str(i) + ") Solo candidatos sin sentencias policiales")
        elif tag == "ageLower":
            print(str(i) + ") Solo candidatos cuya edad sea mayor o igual a " + str(action[2]))
        elif tag == "ageUpper":
            print(str(i) + ") Solo candidatos cuya edad sea menor o igual a " + str(action[2]))
        elif tag == "gender":
            print(str(i) + ") Solo candidatos cuyo género sea " + action[2].lower())
        elif tag == "candidate":
            print(str(i) + ") Solo candidatos cuyo nombre sea " + action[2])
        i += 1

def rerun(data):
    filt = [x for x in data]
    for action in g.get_history():
        print("Performing action " + action[0])
        if (action[0] == "experience" or action[0] == "sentence"):
            filt = action[1](filt)
        else:
            filt = action[1](filt, action[2])
    return filt

def printData():
    for i in range(0, len(g.get_articleData())):
        for key, val in g.get_articleData()[i].items():
            print(key[2:] + ": " + val)
        print('\n')
    print('\n')

def scrape(person):
    r = requests.get('http://peruvotoinformado.com/2020/' + person.replace(' ', '-'))
    coverpage = r.content
    soup = BeautifulSoup(coverpage, 'html5lib')

    data = soup.find_all('li', class_='list-group-item')
    if (len(data) == 0):
        print(person + ' no encontrada!')
        return

    image = "http://peruvotoinformado.com/" + soup.find_all('img')[1].get('src')

    newDict = {}
    newDict["A-Nombre"] = person.title()
    newDict["B-Imagen"] = image
    for j in range(0,len(data)):
        [keyN, valN] = data[j].get_text().split(":",1)
        newDict[str(chr(67+j)) + '-' + keyN.strip().lower().title()] = valN.strip().lower().title()
    g.append_to_articleData(newDict)

def main():
    run()

if __name__== "__main__":
  main()
