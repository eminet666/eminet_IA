import os
from dotenv import load_dotenv

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mistralai import Mistral
from datetime import datetime

# Charger le fichier .env
load_dotenv()

# Charger les variables d'environnement
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

# Vérification des clés
if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY n'est pas définie dans les variables d'environnement")
if not GMAIL_USER or not GMAIL_PASSWORD:
    raise ValueError("GMAIL_USER ou GMAIL_PASSWORD manquant")

print(f"API Key chargée : {MISTRAL_API_KEY[:10]}...")  # Affiche les 10 premiers caractères

# Initialiser le client Mistral
client = Mistral(api_key=MISTRAL_API_KEY)

def generate_greek_dialogue():
    prompt = """
    Crée un dialogue en grec moderne (niveau B2) entre Stephanos et Anna, sur un sujet de la vie quotidienne en Grèce.
    Le dialogue doit faire environ une page A4 (environ 500 mots).
    À la fin, ajoute une liste de vocabulaire avec les mots en grec et leur traduction en français.
    Sujet : {sujet}
    """
    
    # Liste de sujets
    sujets = [
        "Les courses au marché", "Un dîner en famille",
        "Une sortie au cinéma", "Un problème de voisinage",
        "Un voyage en bus", "Une discussion sur la météo"
    ]
    sujet = sujets[datetime.now().day % len(sujets)]
    
    # Utilisation de la méthode chat.complete
    chat_response = client.chat.complete(
        model="mistral-small-latest",  # Ou "open-mistral-7b" selon vos besoins
        messages=[{"role": "user", "content": prompt.format(sujet=sujet)}]
    )
    
    return chat_response.choices[0].message.content

def send_email(content):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = "eminet666@gmail.com"
    msg["Subject"] = "Ton dialogue grec quotidien"
    
    msg.attach(MIMEText(content, "plain", "utf-8"))  # Ajout de utf-8 pour le grec
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    dialogue = generate_greek_dialogue()
    print(dialogue)
    send_email(dialogue)