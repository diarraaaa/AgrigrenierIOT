import time
from flask import render_template
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import urllib.parse
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_url = supabase_url.replace("\\x3a", ":") 
#creer un client supabase pour pouvoir acceder au projet(base de données ,authentification,etc)
supabase :Client = create_client(supabase_url, supabase_key)

#cette fonction est utlilisée pour faire une tache automatique dans l'arriere plan sans avoir besoin de l'executer nous meme
def automatictask():
    while True:
        constante=supabase.table('kits').select('temperature,humidite,id_proprio,id_kit').execute()
        for i in range(len(constante.data)):
            temperature=constante.data[i]['temperature']
            humidite=constante.data[i]['humidite']
            id_proprio=constante.data[i]['id_proprio']
            id_kit=constante.data[i]['id_kit']
            if temperature<1000:
                supabase.table('alertes').insert({
                    'id_agriculteur': id_proprio,
                    'id_kit': id_kit,
                    'enonce': "La temperature est trop basse"
                }).execute()
                print("alerte envoyée")
                print(id_kit)
        time.sleep(300)

