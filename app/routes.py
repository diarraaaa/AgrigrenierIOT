from flask  import Flask, render_template,request,jsonify
from app import app
from supabase import create_client, Client
from app.fonctions import deconnection,commanderkit,infokitdetails,alertecode,ajouterculture,boutiquepagecode,enregistrercommandecode,voirmescommandescode,updateculture
import os
from dotenv import load_dotenv
import urllib.parse

@app.route('/')
def index():
    return render_template('accueil.html')
@app.route('/connexionpage')
def connexionpage():
    return render_template('Connection.html')
@app.route('/deconnexion')
def deconnexion():
    return deconnection()
@app.route('/commanderkit', methods=['POST'])
def commanderkitroute():
    return commanderkit()
@app.route('/requestkit',methods=['POST'])
@app.route('/inscriptionpage')
def inscriptionpage():
    return render_template('Inscription.html')
@app.route('/boutiquepage',methods=['Get','POST'])
def boutiquepage():
    return render_template('boutique.html')

@app.route('/boutiquepagecode',methods=['POST'])
def boutiquepagecoderoute():
    return boutiquepagecode()
@app.route('/infokit',methods=['POST'])
def infokitroute():
    return infokitdetails()
@app.route('/tableaudebord')
def tableaudebordpage():
    return render_template('tableaudebord.html')
@app.route('/alertekits' ,methods=['POST'])
def alertespage():
    return alertecode()
@app.route('/commande',methods=['POST'])
def enregistrercommande():
   return enregistrercommandecode()
@app.route('/mescommandes')
def voirmescommandes():
    return voirmescommandescode()

@app.route('/ajouterculture',methods=['POST'])
def ajoutercultureroute():
    return ajouterculture()

@app.route('/monprofil',methods=['Get','POST'])
def monprofil():
    return render_template('monprofil.html')

@app.route('/updateculture',methods=['POST'])
def updatecultureroute():
    return updateculture()

