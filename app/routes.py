from flask  import Flask, render_template
from app import app
from app.fonctions import test,deconnection,commanderkit,requestkit,infokitdetails

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