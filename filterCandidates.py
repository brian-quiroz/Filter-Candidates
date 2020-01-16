import json
from filters import *
from globals import g

def filterData(page):
    NUM_PER_PAGE = 10
    g.reset_articleData()

    selected = rerun(g.get_json_data())
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
