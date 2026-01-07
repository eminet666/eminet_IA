# main.py
# Script principal de l'agent d'apprentissage du grec

import os
from dotenv import load_dotenv
from mistralai import Mistral

# Import des modules locaux
from dialogue_generator import generate_greek_dialogue, extract_title, extract_dialogue_lines
from audio_generator import generate_audio_from_dialogue
from pdf_generator import generate_pdf_from_dialogue
from email_sender import send_email


def main():
    """
    Fonction principale de l'agent
    """
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
    
    print(f"✓ Configuration chargée")
    
    # Initialiser le client Mistral
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    # Générer le dialogue
    print("- Génération du dialogue...")
    dialogue = generate_greek_dialogue(client)
    print(f"✓ Dialogue généré")
    
    # Extraire le titre
    title = extract_title(dialogue)
    if title:
        print(f"✓ Titre extrait : {title}")
    
    # Extraire les répliques pour l'audio
    dialogue_lines = extract_dialogue_lines(dialogue)
    print(f"✓ {len(dialogue_lines)} répliques extraites")
    
    # Générer le fichier audio
    audio_file = None
    if dialogue_lines:
        audio_file = generate_audio_from_dialogue(dialogue_lines, "dialogue_grec.mp3")
    
    # Générer le fichier PDF
    pdf_file = generate_pdf_from_dialogue(dialogue, title, "dialogue_grec.pdf")
    
    # Envoyer l'email avec le dialogue, l'audio, le PDF et le titre
    print("- Envoi de l'email...")
    send_email(GMAIL_USER, GMAIL_PASSWORD, dialogue, audio_file, pdf_file, title)
    print(f"✓ Email envoyé avec audio et PDF en pièces jointes")
    
    # Nettoyer les fichiers locaux
    if audio_file and os.path.exists(audio_file):
        os.remove(audio_file)
        print(f"✓ Fichier audio local nettoyé")
    
    if pdf_file and os.path.exists(pdf_file):
        os.remove(pdf_file)
        print(f"✓ Fichier PDF local nettoyé")


if __name__ == "__main__":
    main()