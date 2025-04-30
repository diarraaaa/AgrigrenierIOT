import time
from flask import render_template
#cette fonction est utlilisée pour faire une tache automatique dans l'arriere plan sans avoir besoin de l'executer nous meme
def automatictask():
    while True:
        print("I am running in the background")
        time.sleep(1)