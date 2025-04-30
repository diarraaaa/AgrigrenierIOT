from flask import Flask
import threading
app = Flask(__name__)
app.secret_key = 'agrigrenierkeysecret'

from app import routes 
from app import fonctions
from app import auth
from app import auto
from app.auto import *
#on utlise le threading pour que le programme puisse executer la tache automatique
threading.Thread(target=auto.automatictask,daemon=True).start()