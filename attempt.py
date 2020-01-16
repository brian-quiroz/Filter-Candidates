import requests
import json
from bs4 import BeautifulSoup
from globals import g

CANDIDATES_PER_PAGE = 100

def scrape(person):
    link = 'http://peruvotoinformado.com/2020/' + person.replace(' ', '-')
    r = requests.get(link)
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
    newDict["H-Link"] = link
    for j in range(0,len(data)):
        [keyN, valN] = data[j].get_text().split(":",1)
        if (keyN.strip() == "INGRESO ANUAL"):
            if (valN[4:] == "" or valN[4:] == "No registra información"):
                print(str(g.get_length_of_articleData()) + ") " + valN + " -> " + str(-1))
                valN = str(-1)
            else:
                print(str(g.get_length_of_articleData()) + ") " + valN + " -> " + valN[4:])
                valN = valN[4:]
        if (keyN.strip() != "GÉNERO"):
            newDict[str(chr(67+j)) + '-' + keyN.strip().lower().title()] = valN.strip().lower().title()
    g.append_to_articleData(newDict)

def run(page):
    g.reset_articleData()

    selected = g.get_json_data()
    g.set_amount(len(selected))
    print("Selected " + str(len(selected)))

    people = [x["Candidato"] for x in selected]
    # print("Results" + str(0 + CANDIDATES_PER_PAGE*(page - 1) + 1) + "through" + str(CANDIDATES_PER_PAGE + CANDIDATES_PER_PAGE*(page -1)))
    # sample = people[0 + CANDIDATES_PER_PAGE*(page - 1):CANDIDATES_PER_PAGE + CANDIDATES_PER_PAGE*(page - 1)]

    for i in range(0, len(people)):
        scrape(people[i].lower())
    print("Article data: " + str(len(g.get_articleData())))

    printData();

    newJsonData = json.dumps(g.get_articleData(), ensure_ascii=False)
    filename = "scrapedCandidates.json"
    with open(filename, 'w') as f:
        f.write(newJsonData)
        f.close()

def printData():
    for i in range(0, len(g.get_articleData())):
        for key, val in g.get_articleData()[i].items():
            if (key[2:] == "Nombre"):
                print(str(i) + ") " + key[2:] + ": " + val)
    print('\n')

def main():
    run(1)

if __name__== "__main__":
  main()
