"""

This program contain two rest service action with post http method.

It gives the original information of covid cases in India.

It call another get rest service and then filtering the data with the state codes.

Second service calls the json file and read and update the information to the file.


"""

from flask import Flask, jsonify
from flask import request
import requests
import json

app = Flask(__name__)

"""
This method returns the data as json object
"""


def allData(data):
    return jsonify(data)


"""
This method accept the data and returns the data with state wise as a json format.
"""


def statesData(data):
    totalactive = 0
    totalconfirmed = 0
    totalrecovered = 0
    for key in data:
        for i in range(0, len(data[key])):
            totalactive += data[key][i]["active"]
            totalconfirmed += data[key][i]["confirmed"]
            totalrecovered += data[key][i]["recovered"]

    data.update({'totalActiveCases': totalactive})
    data.update({'totalConfirmedCases': totalconfirmed})
    data.update({'totalRecoveredCases': totalrecovered})
    return jsonify(data)


"""
Filtering the data with specific state code
"""


def specificState(data, scode):
    totalactive = 0
    totalconfirmed = 0
    totalrecovered = 0
    for i in range(0, len(data[scode])):
        totalactive += data[scode][i]["active"]
        totalconfirmed += data[scode][i]["confirmed"]
        totalrecovered += data[scode][i]["recovered"]

    display = data[scode]

    total = [{
        'totalActiveCases': totalactive,
        'totalConfirmedCases': totalconfirmed,
        'totalRecoveredCases': totalrecovered
    }]

    display.append(total)
    return jsonify(display)


"""
this action excepts the header information an two request parameters and return the data with required request params.
"""


@app.route('/getStateData', methods=['POST'])
def getData():
    username = request.headers.get('username')
    password = request.headers.get('password')
    token = request.headers.get('token')

    if username == "" and password == "" and token == "":
        return "provide the header values"
    elif username == "python" and password == "PYTHON" and token == "abcd":
        if not request.json:
            return "Pass the request parameters"
        url = 'https://api.covid19india.org/v2/state_district_wise.json'
        covidResponse = requests.get(url)
        data = json.loads(covidResponse.content)
        scode = request.json['scode']
        total = request.json['total']

        stateCodes = []
        districtdata = []
        for i in range(0, len(data)):
            stateCodes.append(data[i]["statecode"])
            districtdata.append(data[i]["districtData"])
        dictonary = dict(zip(stateCodes, districtdata))

        if (scode == "ALL" or scode == "") and (total == "" or total == "N"):
            return allData(data)
        elif (scode == "ALL" or scode == "") and total == "Y":
            return statesData(dictonary)
        elif scode in dictonary.keys() and (total == "" or total == "N"):
            return jsonify(dictonary[scode])
        elif scode in dictonary.keys() and total == "Y":
            return specificState(dictonary, scode)
        else:
            return "Provide valid request"

    else:
        return "Invalid username and password"


"""
It reads data from json fine and update the json file with the request details.
"""


@app.route('/writeData', methods=['POST'])
def writedata():
    username = request.headers.get('username')
    password = request.headers.get('password')
    token = request.headers.get('token')

    if username == "" and password == "" and token == "":
        return "provide the header values"
    elif username == "python" and password == "PYTHON" and token == "abcd":
        file = open('data.json', )
        data = json.load(file)
        if not request.json:
            return "provide the request to write"

        case = {
            "active": request.json['active'],
            "confirmed": request.json['confirmed'],
            "county": request.json['county'],
            "state": request.json['state'],
            "recovered": request.json['recovered']
        }

        data.append(case)
        fp = open('data.json', 'w')
        json.dump(data, fp)
        fp.close()
        file.close()
        return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
