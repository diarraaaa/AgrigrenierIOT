from flask import Flask, render_template, request, redirect, url_for,session
from app import app
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from twilio.rest import Client as TwilioClient
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
        return render_template('Connection.html', message="La valeur est supérieure  à 100")
    else:
        return render_template('Connection.html', message="La valeur est inférieure à 100")

def deconnection():
    session.clear()
    return render_template('Inscription.html')

def commanderkit():
    session['id']=request.form['userid']
    session['prenom']=request.form['userprenom']

    return render_template('commanderkit.html',session=session)

def requestkit():
    session['id']=request.form['userid']
    commande=random.randint(1,100000000)

    supabase.table('commandes').insert({
        'id_agriculteur': session['id'],
        'id_commande':commande
    }).execute()

    #envoyer un mail de confirmation de la commande
    expediteur=os.getenv("SENDER")
    mot_de_passe=os.getenv("PASSWORD")
    destinataire=session['email']
    #remplir les information du mail
    email=MIMEMultipart()
    email['From']=expediteur
    email['To']=destinataire
    email['Subject']="Commande de kit Agrigrenier"
    contenu=f"Bonjour {session['prenom']}.Merci d'avoir effectué une commande sur notre site.Un agent vous contactera d'ici 24 heures pour la finalisation Merci de de votre confiance"
    #creer le mail
    email.attach(MIMEText(contenu,'plain'))
    #envoyer le mail
    try:
        with smtplib.SMTP('smtp.gmail.com',587) as serveur:
            #securiser la connexion
            serveur.starttls()
            #se connecter au serveur 
            serveur.login(expediteur,mot_de_passe)
            #envoyer le email
            serveur.send_message(email)
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'envoi de l'email: {e}")

    #envoyer un message de confirmation de la commande
    #creation du client twilio 
    twilioclient=TwilioClient(os.getenv('twilio_sid'),os.getenv('twilio_token'))
    #remplir les information du message
    message=f"Bonjour {session['prenom']}.Merci d'avoir effectué une commande sur notre site.Un agent vous contactera d'ici 24 heures pour la finalisation Merci de de votre confiance"
    try:
        #envoyer le message 
        twilioclient.messages.create(
            body=message,
            from_=os.getenv('mynumber'),
            to="+221"+session['telephone']
        )
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'envoi du message: {e}")
   
    return render_template('commanderkitdone.html',session=session)
