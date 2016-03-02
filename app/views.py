from app import app, db
from flask import request, jsonify, Response, make_response
from models import DotImage
import aux
import datetime, json, base64, tempfile, tarfile, os
import ipdb

@app.route('/getData', methods=['POST'])
def sendResponse():
    
    data = json.loads(request.data)
    
    dateLst = aux.getDates(data['startDate'], data['endDate'])
    timeLst = aux.getTimes(data['startTime'], data['endTime'])
        
    if data['weatherStatus'] == 'All':
        rain = None
    elif data['weatherStatus'] == 'Rainy':
        rain = 1
    else:
        rain = 0

    if data['limit'] == "" or data['limit'] is None:
        limit = None

    if data['location'] == "" or data['location'] is None:
        location = None
    else:
        location = data['location']

    limit = int(data['limit']) if (data['limit'] is not None and data['limit'].isdigit()) else None
        
    if type(dateLst) == str:
        return jsonify(err=dateLst)
    
    elif type(timeLst) == str:
        return jsonify(err=timeLst)
    
    else:
        startTime, endTime = timeLst
        startDate, endDate = dateLst

        results = aux.getResults(db, startDate, endDate, startTime, endTime, location, rain, limit)
        print results.count()
        def generate():
            if results.count():
                for row in results:
                    item = dict()
                    item['imgId'] = str(row.id).encode('utf8')
                    item['location'] = str(row.locationId).encode('utf8')
                    item['date'] = str(row.date).encode('utf8')
                    item['time'] = str(row.time).encode('utf8')
                    item['rain'] = str(row.rain).encode('utf8')

                    #get image dataurl
                    path = str(row.path)
                    dataUrl = u''.join(base64.encodestring(open(path).read()).splitlines())
                    item['dataUrl'] = "data:image/jpg;base64, " + dataUrl



                    yield json.dumps(item) + ','
            else:
                yield json.dumps('{}') + ','
        return Response(generate(), mimetype='text')

@app.route('/prepareDownload', methods=["POST"])
def prepareFile():

    #Get ids from request
    ids = [int(n) for n in request.get_json(force=True)['ids']]    

    #Get results
    results = db.session.query(DotImage).filter(DotImage.id.in_(ids))



    #Compress to tarball
    tar = tarfile.open(fileobj=tempfile.NamedTemporaryFile(delete=False), mode='w:gz') 
    for i, row in zip(range(0, results.count()), results):
        tar.add(row.path, arcname="img" + str(i) + ".jpg")
    fullPath = tar.name
    tar.close()
    
    #Rename the file
    path = '/'.join(fullPath.split('/')[:-1]) + '/'
    filename = fullPath.split('/')[-1]
    os.rename(fullPath, fullPath + '.tar.gz')

    return jsonify({'filename':filename})

    
@app.route('/download/<filename>', methods=["GET"])
def download(filename):
    #Read file
    f=open(app.config['UPLOAD_FOLDER'] + '/' + filename +'.tar.gz', 'rb')
    content = f.read()
    f.close()
    
    #Create response and download
    response = make_response(content)
    response.headers["Content-Disposition"] = "attachment; filename=images.tar.bz"
    return response