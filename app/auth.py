from flask import Flask, render_template, request, session
from app import app
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from supabase import create_client, Client
#Récuperer les variables d'environnement dans le fichier .env
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)

@app.route('/inscrirecode', methods=['POST'])
def inscrirecode():
    nom= request.form['nom']
    prenom= request.form['prenom']
    email= request.form['email']
    motdepasse= request.form['motdepasse']
    confirmotdepasse=request.form['confirm_motdepasse']
    region= request.form['region']
    telephone= request.form['telephone']
    #Vérifier si les mots de passe sont identiques
    if motdepasse!= confirmotdepasse:
        return render_template('index.html',message="Les mots de passe doivent etre identiques")
    if len(motdepasse)<6:
        return render_template('index.html',message="Le mot de passe doit contenir au moins 6 caractères")
    motdepasse= generate_password_hash(motdepasse)
    #Vérifier si l'email existe déjà
    verif_email=supabase.table('profiles').select('email').eq('email',email).execute()
    if verif_email.data:
        return render_template('index.html',message="L'email existe deja.Veuillez vous connecter")
    #Inscription dans la base de données
    supabase.table('profiles').insert({
      'nom': nom,
      'prenom': prenom,
      'email': email,
      'motdepasse': motdepasse,
      'region': region,
      'telephone': telephone
    }).execute()                                  
    return render_template('index.html')

@app.route('/connexioncode', methods=['POST'])
def connexioncode():
    email=request.form['email']
    motdepasse=request.form['motdepasse']
    #Vérifier si l'email est dans la base
    emailpresent=supabase.table('profiles').select("email").eq('email',email).execute()
    if not emailpresent.data:
        return render_template('test.html',message="L'email n'existe pas.Veuillez vous inscrire")
    #Vérifier si le mot de passe est correct
    motdepassecorrect=supabase.table('profiles').select('motdepasse').eq('email',email).execute()
    motdepassecorrect=motdepassecorrect.data[0]['motdepasse']
    motdepassecorrect=check_password_hash(motdepassecorrect,motdepasse)
    if not motdepassecorrect:
        return render_template('test.html',message="Le mot de passe est incorrect")
    
    #Maintenant on recupére les infos de l'utilisateur

    infos=supabase.table('profiles').select("*").eq('email',email).execute()
    prenom=infos.data[0]['prenom']
    id=infos.data[0]['id']
    region=infos.data[0]['region']  

    #Je crée les variables de session
    session['prenom']=prenom
    session['email']=email
    session['id']=id
    session['region']=region

    #Apres avoir stocké les infos je peux enfin le rediriger vers son tableau de bord
    return render_template('tableaudebord.html',session=session)