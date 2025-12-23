import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from mistralai import Mistral
# from datetime import datetime
from dotenv import load_dotenv

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