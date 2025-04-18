from flask import Flask

app = Flask(__name__)
app.secret_key = 'agrigrenierkeysecret'

from app import routes 
from app import fonctions
from app import auth
