from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost:3306/nanotech'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

load_dotenv()

accessKey = os.getenv('accessKey')
secretKey = os.getenv('secretKey')
region = os.getenv('region')
bucket_name = os.getenv('bucket_name')
