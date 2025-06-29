import time
from flask import render_template,session
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from twilio.rest import Client as TwilioClient

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_url = supabase_url.replace("\\x3a", ":") 
#creer un client supabase pour pouvoir acceder au projet(base de données ,authentification,etc)
supabase :Client = create_client(supabase_url, supabase_key)

#cette fonction est utlilisée pour faire une tache automatique dans l'arriere plan sans avoir besoin de l'executer nous meme
def automatictask():
    while True:
        constante=supabase.table('kits').select('temperature,humidite,id_proprio,id_kit,nom').execute()
        for i in range(len(constante.data)):
            temperature=constante.data[i]['temperature']
            humidite=constante.data[i]['humidite']
            id_proprio=constante.data[i]['id_proprio']
            nomkit=constante.data[i]['nom']
            id_kit=constante.data[i]['id_kit']
            #recuperer le nom et le num du proprio
            infosproprio=supabase.table('profiles').select('nom,prenom,telephone').eq('id',id_proprio).execute()
            tel=infosproprio.data[0]['telephone']
            prenom=infosproprio.data[0]['prenom']
            nom=infosproprio.data[0]['nom']
             #recuperer les cultures qui sont dans le kit
            cultures=supabase.table('kit_culture').select('id_culture').eq('id_kit',id_kit).execute()
            for i in range(len(cultures.data)):
                id_culture=cultures.data[i]['id_culture']
                #recuperer le nom et les constantes de chaque culture
                infos=supabase.table('culture').select('*').eq('id_culture',id_culture).execute()
                tempmin=infos.data[0]['temperaturemin']
                tempmax=infos.data[0]['temperaturemax']
                humiditemin=infos.data[0]['humiditemin']
                humiditemax=infos.data[0]['humiditemax']
                alerte=""
                if temperature>tempmax:
                    supabase.table('alertes').insert({
                        'id_agriculteur': id_proprio,
                        'id_kit': id_kit,
                        'enonce': "La température est trop élevée pour "+ infos.data[0]['nom']
                    }).execute()
                    alerte="La température est trop élevée pour "+ infos.data[0]['nom']
                    print("alerte temperature envoyée")

                else:
                    if temperature<tempmin:
                        supabase.table('alertes').insert({
                            'id_agriculteur': id_proprio,
                            'id_kit': id_kit,
                            'enonce': "La température est trop basse pour "+ infos.data[0]['nom']
                        }).execute()
                        alerte="La température est trop basse pour "+ infos.data[0]['nom']
                        print("alerte temperature envoyée")

                if humidite>humiditemax:
                    supabase.table('alertes').insert({
                        'id_agriculteur': id_proprio,
                        'id_kit': id_kit,
                        'enonce': "L'humidité est trop élevée pour "+ infos.data[0]['nom']
                    }).execute()
                    print("alerte humidité envoyée")
                    alerte="L'humidité est trop élevée pour "+ infos.data[0]['nom']
                else :
                    if humiditemin>humidite:
                        supabase.table('alertes').insert({
                            'id_agriculteur': id_proprio,
                            'id_kit': id_kit,
                            'enonce': "L'humidité est trop basse pour "+ infos.data[0]['nom']
                        }).execute()
                        print("alerte humidité envoyée")
                        alerte="L'humidité est trop basse pour "+ infos.data[0]['nom']
                alertes=alerte
                #envoyer un mail de confirmation de la commande
                if alertes:
                    send_alert(nomkit, prenom, nom, tel, alertes)
        time.sleep(1200) #  # Attendre 20 minutes avant de vérifier à nouveau
        
        
def send_alert(nomkit, prenom, nom, tel, alertes):

                infostwilio=supabase.table('keys').select('*').eq('nom',"twillio").execute()
                infostwiliodata=infostwilio.data
                #recuperer les informations de l'api twillio
                username=infostwiliodata[0]['username']
                password=infostwiliodata[0]['password']
                twilioclient=TwilioClient(username,password)
                #remplir les information du message
                message="Bonjour "+prenom+ " "+ nom," Voici votre alerte concernant le kit "+nomkit+" : "+alertes+" Merci de votre confiance.L'équipe de SmartAgriculture"
                try:
                    #envoyer le message 
                    twilioclient.messages.create(
                        body=message,
                        from_=os.getenv('mynumber'),
                        to="+221"+tel
                    )
                except Exception as e:
                    print(f"Une erreur s'est produite lors de l'envoi du message: {e}")
    # Cette fonction est appelée pour envoyer une alerte
    