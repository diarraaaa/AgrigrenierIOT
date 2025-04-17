from flask  import Flask, render_template, request, redirect, url_for
from app import app

@app.route('/')
def index():
    return render_template('index.html')