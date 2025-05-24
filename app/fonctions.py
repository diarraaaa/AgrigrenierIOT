from flask import Flask, render_template, request, redirect, url_for,session,json,jsonify
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
from datetime import datetime


#Récuperer les variables d'environnement dans le fichier .env
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_url = supabase_url.replace("\\x3a", ":") 
supabase_key = supabase_key.replace("\\x3a", ":") 
#creer un client supabase pour pouvoir acceder au projet(base de données ,authentification,etc)
supabase :Client = create_client(supabase_url, supabase_key)

def deconnection():
    session.clear()
    return render_template('Inscription.html')

def commanderkit():
    session['id']=request.form['userid']
    session['prenom']=request.form['userprenom']

    return render_template('commanderkit.html',session=session)


def infokitdetails():
    idkit=request.form['id_kit']
    nomkit=request.form['nomkit']
    session['idkit']=idkit
    #je récupére les informations du kit depuis la base de donnés
    infoskits=supabase.table('kits').select("*").eq('id_kit',idkit).execute()
    temperature=infoskits.data[0]['temperature']
    humidite=infoskits.data[0]['humidite']
    #recuperer les cultures qui sont dans le kit
    cultures=supabase.table('kit_culture').select('id_culture').eq('id_kit',idkit).execute()
    for i in range(len(cultures.data)):
        id_culture=cultures.data[i]['id_culture']
        #recuperer le nom et les constantes de chaque culture
        infos=supabase.table('culture').select('*').eq('id_culture',id_culture).execute()
        nom=infos.data[0]['nom']
        tempmin=infos.data[0]['temperaturemin']
        tempmax=infos.data[0]['temperaturemax']
        humiditemin=infos.data[0]['humiditemin']
        humiditemax=infos.data[0]['humiditemax']
        #on ajoute cette valeur dans les infos de chaque culture
        cultures.data[i]['nom']=nom
        cultures.data[i]['temperaturemin']=tempmin
        cultures.data[i]['temperaturemax']=tempmax
        cultures.data[i]['humiditemin']=humiditemin
        cultures.data[i]['humiditemax']=humiditemax  
        #je recupere la quantité de chaque culture
        quantite=supabase.table('kit_culture').select('quantité').eq('id_kit',idkit).eq('id_culture',id_culture).execute()
        cultures.data[i]['quantité']=quantite.data[0]['quantité']
    contenu=cultures.data
    contenunorme=cultures.data
    #je recupére les alertes au niveau de la base de données
    alertes=supabase.table('alertes').select('*').eq('id_kit',idkit).order('date_alerte',desc=True).limit(15).execute()
    alertes=alertes.data
    alertes=json.dumps(alertes)
    contenu=json.dumps(contenu)
    return render_template('infokit.html',contenu=contenu,session=session,nomkit=nomkit,temperature=temperature,humidite=humidite,alertes=alertes,contenunorme=contenunorme)
def alertecode():
    userid=request.form['userid']
    #je récupére les alertes depuis la base de donnés
    alertes=supabase.table('alertes').select('enonce,id_kit,date_alerte').eq('id_agriculteur',userid).execute()
    for i in range(len(alertes.data)):
        id_kit=alertes.data[i]['id_kit']
        date_alerte=alertes.data[i]['date_alerte']
        #je récupére les kits depuis la base de donnés
        kits=supabase.table('kits').select('nom').eq('id_kit',id_kit).execute()
        alertes.data[i]['nom_kit']=kits.data[0]['nom']
        dt = datetime.fromisoformat(alertes.data[i]['date_alerte'])
        alertes.data[i]['date_alerte']= dt.strftime("%A %d %B %Y à %H :%M %p").capitalize()    
    contenu=alertes.data
    return render_template('Alertes.html',contenu=contenu,session=session)

def ajouterculture():
    idkit=session['idkit']
    nomkit=supabase.table('kits').select('nom').eq('id_kit',idkit).execute()
    infoskits=supabase.table('kits').select("*").eq('id_kit',idkit).execute()
    temperature=infoskits.data[0]['temperature']
    humidite=infoskits.data[0]['humidite']
    nomkit=nomkit.data[0]['nom']
    session['nomkit']=nomkit
    print(idkit)
    culture=request.form['culture']
    print(culture)
    quantite=request.form['quantite']
    print(quantite)
    idculture=supabase.table('culture').select('id_culture').eq('nom',culture).execute()
    idculture=idculture.data[0]['id_culture']
    cultures=supabase.table('kit_culture').select('id_culture').eq('id_kit',idkit).execute()
    for i in range(len(cultures.data)):
            id_culture=cultures.data[i]['id_culture']
            #recuperer le nom et les constantes de chaque culture
            infos=supabase.table('culture').select('*').eq('id_culture',id_culture).execute()
            nom=infos.data[0]['nom']
            tempmin=infos.data[0]['temperaturemin']
            tempmax=infos.data[0]['temperaturemax']
            humiditemin=infos.data[0]['humiditemin']
            humiditemax=infos.data[0]['humiditemax']
            #on ajoute cette valeur dans les infos de chaque culture
            cultures.data[i]['nom']=nom
            cultures.data[i]['temperaturemin']=tempmin
            cultures.data[i]['temperaturemax']=tempmax
            cultures.data[i]['humiditemin']=humiditemin
            cultures.data[i]['humiditemax']=humiditemax
            #je recupere la quantité de chaque culture
            quantite=supabase.table('kit_culture').select('quantité').eq('id_kit',idkit).eq('id_culture',id_culture).execute()
            cultures.data[i]['quantité']=quantite.data[0]['quantité']
        
    contenu=cultures.data
    contenunorme=cultures.data
    #je recupére les alertes au niveau de la base de données
    alertes=supabase.table('alertes').select('*').eq('id_kit',idkit).order('date_alerte',desc=True).limit(15).execute()
    alertes=alertes.data
    alertes=json.dumps(alertes)
    contenu=json.dumps(contenu)
    #regarder si la culture est déjà dans le kit
    culturepresent=supabase.table('kit_culture').select('id_culture').eq('id_kit',idkit).eq('id_culture',idculture).execute()
    if culturepresent.data:
        return render_template('infokit.html',session=session,nomkit=session['nomkit'],culturepresent="Cette culture est déjà présente dans le kit .Veuillez juste mettre à jour la quantité",alertes=alertes,contenu=contenu,temperature=temperature,humidite=humidite,contenunorme=contenunorme)
    #ajouter la culture dans la table kit_culture
    supabase.table('kit_culture').insert({
        'id_kit': idkit,
        'id_culture': idculture,
        'quantité': quantite
    }).execute()
    return render_template('infokit.html',session=session,nomkit=session['nomkit'],cultureajoute="Votre culture a été ajoutée avec succés",alertes=alertes,contenu=contenu,temperature=temperature,humidite=humidite,contenunorme=contenunorme)
    #ajouter la culture dans la table kit_culture

def boutiquepagecode():
    session['id']=request.form['userid']
    userid=session['id']
    return render_template('boutique.html',session=session,userid=userid)

def enregistrercommandecode():
    info_commande=request.get_json()
    print(info_commande)
    idcommande=random.randint(1,100000000)
    if info_commande:
        supabase.table('commandes').insert({
            'id_agriculteur': info_commande['userId'],
            'id_commande': idcommande,
            'date_commande': info_commande['date'],
            'montant': info_commande['total'],
            'éléments': info_commande['items'],
            'methode': info_commande['paymentMethod']
        }).execute()

        #envoyer un mail de confirmation de la commande
        infostwilio=supabase.table('keys').select('*').eq('nom',"twillio").execute()
        infostwiliodata=infostwilio.data
        #recuperer les informations de l'api twillio
        username=infostwiliodata[0]['username']
        password=infostwiliodata[0]['password']
        twilioclient=TwilioClient(username,password)
        #remplir les information du message
        message=f"Bonjour {session['prenom']}.Merci d'avoir effectué une commande sur notre site.Un agent vous contactera d'ici 24 heures pour la finalisation.Merci de de votre confiance"
        try:
            #envoyer le message 
            twilioclient.messages.create(
                body=message,
                from_=os.getenv('mynumber'),
                to="+221"+session['telephone']
            )
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'envoi du message: {e}")
        expediteur=os.getenv("SENDER")
        mot_de_passe=os.getenv("PASSWORD")
        destinataire=session['email']
        #Remplir les informations du mail
        email=MIMEMultipart()
        email['From']=expediteur
        email['To']=destinataire
        email['Subject']="Commande de kit Agrigrenier"
        contenu=f"Bonjour {session['prenom']}.Merci d'avoir effectué une commande sur notre site.Un agent vous contactera d'ici 24 heures pour la finalisation .Merci de de votre confiance"
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
        
        return jsonify({"message":"commande enregistrée","status":"success"})
    else:
        return jsonify({"message":"Commande non enregistrée","status":"error"})

def voirmescommandescode():
    id=session['id']
    commandes=supabase.table('commandes').select('*').eq('id_agriculteur',id).execute()
    commandes=commandes.data
    livré=0
    enattente=0
    for i in range(len(commandes)):
        if commandes[i]['Livré'] ==False:
            enattente+=1
        elif commandes[i]['Livré'] ==True:
            livré+=1
    return render_template('mescommandes.html',session=session,commandes=commandes,livré=livré,enattente=enattente)

def updateculture():
    nomculture=request.form['nom']
    idkit=session['idkit']
    quantité=request.form['newquantite']
    
    idculture=supabase.table('culture').select('id_culture').eq('nom',nomculture).execute()
    idculture=idculture.data[0]['id_culture']
    #je met à jour la quantité de la culture
    try:
        supabase.table('kit_culture').update({
            'quantité': quantité
        }).eq('id_kit',idkit).eq('id_culture',idculture).execute()
        infoskits=supabase.table('kits').select("*").eq('id_kit',idkit).execute()
        temperature=infoskits.data[0]['temperature']
        humidite=infoskits.data[0]['humidite']
        #recuperer les cultures qui sont dans le kit
        cultures=supabase.table('kit_culture').select('id_culture').eq('id_kit',idkit).execute()
        for i in range(len(cultures.data)):
            id_culture=cultures.data[i]['id_culture']
            #recuperer le nom et les constantes de chaque culture
            infos=supabase.table('culture').select('*').eq('id_culture',id_culture).execute()
            nom=infos.data[0]['nom']
            tempmin=infos.data[0]['temperaturemin']
            tempmax=infos.data[0]['temperaturemax']
            humiditemin=infos.data[0]['humiditemin']
            humiditemax=infos.data[0]['humiditemax']
            #on ajoute cette valeur dans les infos de chaque culture
            cultures.data[i]['nom']=nom
            cultures.data[i]['temperaturemin']=tempmin
            cultures.data[i]['temperaturemax']=tempmax
            cultures.data[i]['humiditemin']=humiditemin
            cultures.data[i]['humiditemax']=humiditemax  
            #je recupere la quantité de chaque culture
            quantite=supabase.table('kit_culture').select('quantité').eq('id_kit',idkit).eq('id_culture',id_culture).execute()
            cultures.data[i]['quantité']=quantite.data[0]['quantité']
        contenu=cultures.data
        contenunorme=cultures.data
        #je recupére les alertes au niveau de la base de données
        alertes=supabase.table('alertes').select('*').eq('id_kit',idkit).order('date_alerte',desc=True).limit(15).execute()
        alertes=alertes.data
        alertes=json.dumps(alertes)
        contenu=json.dumps(contenu)
        #je recupére l'id de la culture
    except Exception as e:
        print(f"Une erreur s'est produite lors de la mise à jour de la culture: {e}")
        return render_template('infokit.html',session=session,nomkit=session['nomkit'],culturepresent="Erreur lors de la mise à jour de la culture",alertes=alertes,contenu=contenu,temperature=temperature,humidite=humidite,contenunorme=contenunorme)
    
    infoskits=supabase.table('kits').select("*").eq('id_kit',idkit).execute()
    temperature=infoskits.data[0]['temperature']
    humidite=infoskits.data[0]['humidite']
    #recuperer les cultures qui sont dans le kit
    cultures=supabase.table('kit_culture').select('id_culture').eq('id_kit',idkit).execute()
    for i in range(len(cultures.data)):
        id_culture=cultures.data[i]['id_culture']
        #recuperer le nom et les constantes de chaque culture
        infos=supabase.table('culture').select('*').eq('id_culture',id_culture).execute()
        nom=infos.data[0]['nom']
        tempmin=infos.data[0]['temperaturemin']
        tempmax=infos.data[0]['temperaturemax']
        humiditemin=infos.data[0]['humiditemin']
        humiditemax=infos.data[0]['humiditemax']
        #on ajoute cette valeur dans les infos de chaque culture
        cultures.data[i]['nom']=nom
        cultures.data[i]['temperaturemin']=tempmin
        cultures.data[i]['temperaturemax']=tempmax
        cultures.data[i]['humiditemin']=humiditemin
        cultures.data[i]['humiditemax']=humiditemax  
        #je recupere la quantité de chaque culture
        quantite=supabase.table('kit_culture').select('quantité').eq('id_kit',idkit).eq('id_culture',id_culture).execute()
        cultures.data[i]['quantité']=quantite.data[0]['quantité']
    contenu=cultures.data
    contenunorme=cultures.data
    #je recupére les alertes au niveau de la base de données
    alertes=supabase.table('alertes').select('*').eq('id_kit',idkit).order('date_alerte',desc=True).limit(15).execute()
    alertes=alertes.data
    alertes=json.dumps(alertes)
    contenu=json.dumps(contenu)
    #je recupére l'id de la culture
    return render_template('infokit.html',session=session,nomkit=session['nomkit'],cultureajoute="Votre culture a été mise à jour avec succés",alertes=alertes,contenu=contenu,temperature=temperature,humidite=humidite,contenunorme=contenunorme)
