from flask import Flask, render_template, request, redirect, url_for,session
from app import app
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import random
from random import randint

#Récuperer les variables d'environnement dans le fichier .env
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
#creer un client supabase pour pouvoir acceder au projet(base de données ,authentification,etc)
supabase :Client = create_client(supabase_url, supabase_key)


def test():
    valeur= request.form['valeur']
    valeur= int(valeur)

    if valeur> 100:
        return render_template('test.html', message="La valeur est supérieure  à 100")
    else:
        return render_template('test.html', message="La valeur est inférieure à 100")

def deconnection():
    session.clear()
    return render_template('index.html')

def commanderkit():
    session['id']=request.form['userid']
    session['prenom']=request.form['userprenom']

    return render_template('commanderkit.html',session=session)

def requestkit():
    session['id']=request.form['userid']
    commande=random.randint(1,10000000000)

    supabase.table('commandes').insert({
        'id_agriculteur': session['id'],
        'id_commande':commande
    }).execute()

    return render_template('commanderkitdone.html',session=session)
