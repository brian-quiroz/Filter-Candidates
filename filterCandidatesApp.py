import sys
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
    val = int(g.get_regions().index(request.get_json()['val'])) + 1
    g.append_to_history(["regions", lambda selected, ind: filterRegions(selected, ind), val])
    print(request.get_json())  # parse as JSON
    return 'OK', 200

@app.route('/test')
def test_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
