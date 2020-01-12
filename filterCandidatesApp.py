import sys
import json
from params import *
from filters import *
from filterCandidates import run2
from globals import g
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/candidatesData', methods=['GET'])
def candidatesData():
    message = run2()
    return jsonify(message)

@app.route('/regions', methods=['GET'])
def regions():
    message = g.get_regions()
    return jsonify(message)

@app.route('/updateRegions', methods=['POST'])
def updateRegions():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    val = int(g.get_regions().index(request.get_json()['val'])) + 1
    g.append_to_history(["regions", lambda selected, ind: filterRegions(selected, ind), val])
    return 'OK', 200

@app.route('/parties', methods=['GET'])
def parties():
    message = g.get_parties()
    return jsonify(message)

@app.route('/updatePartiesIncl', methods=['POST'])
def updatePartiesIncl():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    arr = request.get_json()['val']
    val = list(map(lambda x: int(g.get_parties().index(x)) + 1, arr))
    g.append_to_history(["partiesIncl", lambda selected, ind: filterPartiesIncl(selected, ind), val])
    return 'OK', 200

@app.route('/updatePartiesExcl', methods=['POST'])
def updatePartiesExcl():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    arr = request.get_json()['val']
    val = list(map(lambda x: int(g.get_parties().index(x)) + 1, arr))
    g.append_to_history(["partiesExcl", lambda selected, ind: filterPartiesExcl(selected, ind), val])
    return 'OK', 200

@app.route('/updateExperience', methods=['POST'])
def updateExperience():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    val = request.get_json()
    g.append_to_history(["experience", lambda selected: filterExperience(selected), val])
    return 'OK', 200

@app.route('/studies', methods=['GET'])
def studies():
    message = g.get_studies()
    return jsonify(message)

@app.route('/updateStudies', methods=['POST'])
def updateStudies():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    val = int(g.get_studies().index(request.get_json()['val'])) + 1
    g.append_to_history(["studies", lambda selected, level: filterStudies(selected, level), val])
    return 'OK', 200

@app.route('/updateSentence', methods=['POST'])
def updateSentence():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    val = request.get_json()
    g.append_to_history(["sentence", lambda selected: filterSentence(selected), val])
    return 'OK', 200

@app.route('/updateAgeLower', methods=['POST'])
def updateAgeLower():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    val = int(request.get_json()['val'])
    g.append_to_history(["ageLower", lambda selected, lower: filterAgeLower(selected, lower), val])
    return 'OK', 200

@app.route('/updateAgeUpper', methods=['POST'])
def updateAgeUpper():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    val = int(request.get_json()['val'])
    g.append_to_history(["ageUpper", lambda selected, upper: filterAgeUpper(selected, upper), val])
    return 'OK', 200

@app.route('/updateGender', methods=['POST'])
def updateGender():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    val = str(request.get_json()['val'])
    g.append_to_history(["gender", lambda selected, gender: filterGender(selected, gender), val])
    return 'OK', 200

@app.route('/updateCandidate', methods=['POST'])
def updateCandidate():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    val = str(request.get_json()['val'])
    g.append_to_history(["candidate", lambda selected, name: filterCandidate(selected, name), val])
    return 'OK', 200

@app.route('/test')
def test_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
