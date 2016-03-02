from flask import Flask
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = "/var/folders/zj/55tydjfj3p53bccqkdpxm_3c0000gn/T"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object('config')
db = SQLAlchemy(app)

#TOTO: REMOVE CORS
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

from app import views, models