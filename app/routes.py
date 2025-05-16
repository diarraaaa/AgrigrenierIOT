from flask  import Flask, render_template,request,jsonify
from app import app
from supabase import create_client, Client
from app.fonctions import test,deconnection,commanderkit,infokitdetails,alertecode,ajouterculture,boutiquepagecode,enregistrercommandecode
import os
from dotenv import load_dotenv
import urllib.parse
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_url = supabase_url.replace("\\x3a", ":") 
supabase: Client = create_client(supabase_url, supabase_key)
@app.route('/')

def index():
    return render_template('accueil.html')
@app.route('/test', methods=['POST'])
def testvaleur():
    return test()
@app.route('/testpage')
def testpage():
    return render_template('Connection.html')
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
def requestkitroute():
    return requestkit()
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