from flask import Flask, render_template, request, redirect, url_for
from app import app
import os
from dotenv import load_dotenv
from supabase import create_client, Client

#Récuperer les variables d'environnement dans le fichier .env
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")


def test():
    valeur= request.form['valeur']
    valeur= int(valeur)

    if valeur> 100:
        return render_template('test.html', message="La valeur est supérieure  à 100")
    else:
        return render_template('test.html', message="La valeur est inférieure à 100")
    