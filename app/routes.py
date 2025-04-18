from flask  import Flask, render_template
from app import app
from app.fonctions import test

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/test', methods=['POST'])
def testvaleur():
    return test()
@app.route('/testpage')
def testpage():
    return render_template('test.html')
@app.route('/connexionpage')
def connexionpage():
    return render_template('test.html')