from app import app, db
from flask import render_template, url_for, request, jsonify, Response, stream_with_context
from models import DotImage
import datetime
import aux
import json
import ipdb
@app.route('/')
def index():
    return render_template('index.html',a="AAA")


@app.route('/getData1', methods=["GET", "POST"])
def getData():
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    location = request.args.get('location')
    limit = request.args.get('limit')
    weatherStatus = request.args.get('weatherStatus')
    startTime = request.args.get('startTime')
    endTime = request.args.get('endTime')

    dateLst = aux.getDates(startDate, endDate)
    timeLst = aux.getTimes(startTime, endTime)
    # ipdb.set_trace()
    print request.args
    if weatherStatus == 'All':
        rain = None

    elif weatherStatus == 'Rainy':
        rain = 1
    else:
        rain = 0

    if limit == "":
        limit = None

    if location == "":
        location = None

    limit = int(limit) if limit.isdigit() else None
        
    if type(dateLst) == str:
        return jsonify(err=dateLst)
    
    elif type(timeLst) == str:
        return jsonify(err=timeLst)
    
    else:
        startTime, endTime = timeLst
        startDate, endDate = dateLst

        results = aux.getResults(db, startDate, endDate, startTime, endTime, location, rain, limit)
        
        resultsList = []

        for item in  results:
            temp = dict()
            temp['id'] = item.id
            temp['location'] = item.locationId
            temp['rain'] = item.rain
            temp['date'] = item.date.strftime("%m/%d/%Y")
            temp['time'] = item.time.strftime("%H:%M:%S")
            
            resultsList.append(temp)
        
        return jsonify(images=resultsList)

@app.route('/getData', methods=['GET', 'POST'])
def sendResponse():
    # ipdb.set_trace()
    data = json.loads(request.data)
    dateLst = aux.getDates(data['startDate'], data['endDate'])
    timeLst = aux.getTimes(data['startTime'], data['endTime'])
    
    
    if data['weatherStatus'] == 'All':
        rain = None

    elif data['weatherStatus'] == 'Rainy':
        rain = 1
    else:
        rain = 0

    if data['limit'] == "":
        limit = None

    if data['location'] == "":
        location = None

    limit = int(data['limit']) if (data['limit'] is not None and data['limit'].isdigit()) else None
        
    if type(dateLst) == str:
        return jsonify(err=dateLst)
    
    elif type(timeLst) == str:
        return jsonify(err=timeLst)
    
    else:
        startTime, endTime = timeLst
        startDate, endDate = dateLst

        results = aux.getResults(db, startDate, endDate, startTime, endTime, location, rain, limit)
        
        def generate():
            if results.count():
                for row in results:
                    item = dict()
                    item['imgId'] = str(row.id).encode('utf8')
                    item['location'] = str(row.locationId).encode('utf8')
                    item['date'] = str(row.date).encode('utf8')
                    item['time'] = str(row.time).encode('utf8')
                    item['rain'] = str(row.rain).encode('utf8')
                    yield json.dumps(item) + ','
            else:
                yield json.dumps('{}') + ','
        return Response(generate(), mimetype='text')
