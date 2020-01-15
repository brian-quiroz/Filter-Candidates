import sys
import json
from filters import *
from filterCandidates import run2
from globals import g
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/candidatesData', methods=['GET'])
def candidatesData():
    message = run2(g.get_page())
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

@app.route('/history', methods=['GET'])
def history():
    hist = g.get_history()
    actions = [x[0] for x in hist]
    vals = [x[2] for x in hist]
    message = []
    for action, val in zip(actions, vals):
        message.append(g.get_tag_text(action, val))
    return jsonify(message)

@app.route('/delAction', methods=['POST'])
def delAction():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    val = int(request.get_json()['ind'])
    g.del_from_history(val)
    return 'OK', 200

@app.route('/amount', methods=['GET'])
def amount():
    message = g.get_amount()
    return jsonify(message)

@app.route('/currentPage', methods=['GET'])
def currentPage():
    message = g.get_page()
    return jsonify(message)

@app.route('/pageChange', methods=['POST'])
def pageChange():
    print('Incoming!!..')
    print(request.get_json())  # parse as JSON
    val = int(request.get_json()['val'])
    g.set_page(g.get_page() + val)
    print("New page: " + str(g.get_page()))
    return 'OK', 200

@app.route('/goToPageN', methods=['POST'])
def goToPageN():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    val = int(request.get_json()['val'])
    g.set_page(val)
    return 'OK', 200

@app.route('/saveCandidates', methods=['POST'])
def saveCandidates():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    inds = request.get_json()['inds']
    vals = list(map(lambda ind: g.get_articleData()[ind], inds))
    for val in vals:
        g.append_to_saved(val)
    print(len(g.get_saved()))
    return 'OK', 200

@app.route('/saved', methods=['GET'])
def saved():
    message = g.get_saved()
    return jsonify(message)

@app.route('/delCandidate', methods=['POST'])
def delCandidate():
    print('Incoming..')
    print(request.get_json())  # parse as JSON
    ind = int(request.get_json()['ind'])
    val = g.get_saved()[ind]
    print("Deleting " + val["A-Nombre"])
    g.del_from_saved(ind)
    print(len(g.get_saved()))
    return 'OK', 200

@app.route('/test')
def test_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
