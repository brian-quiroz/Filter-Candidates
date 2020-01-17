import json
from filters import *
from globals import g

def filterData(page):
    NUM_PER_PAGE = g.get_NUM_PER_PAGE()
    g.reset_articleData()

    selected = runFiltersAndSort(g.get_json_data())
    g.set_amount(len(selected))
    print("Selected " + str(len(selected)))

    people = [x["Candidato"] for x in selected]
    print("Results " + str(0 + NUM_PER_PAGE*(page - 1) + 1) + " thru " + str(NUM_PER_PAGE + NUM_PER_PAGE*(page -1)))
    sample = people[0 + NUM_PER_PAGE*(page - 1):NUM_PER_PAGE + NUM_PER_PAGE*(page - 1)]

    for i in range(0, len(sample)):
        getScrapedData(sample[i].lower().title())
    print("Article data: " + str(len(g.get_articleData())))
    return g.get_articleData()

def getScrapedData(person):
    matches = [x for x in g.get_scraped_data() if x["A-Nombre"] == person]
    print(len(matches))
    if (len(matches) > 0):
        g.append_to_articleData(matches[0])

def runFiltersAndSort(data):
    filt = [x for x in data]
    for action in g.get_history():
        print("Performing action " + action[0])
        filt = action[1](filt, action[2])
    for action in g.get_ordering_history():
        print ("Performing action " + action[0])
        filt = action[1](filt)
    return filt

def printData():
    for i in range(0, len(g.get_articleData())):
        for key, val in g.get_articleData()[i].items():
            print(key[2:] + ": " + val)
        print('\n')
    print('\n')
