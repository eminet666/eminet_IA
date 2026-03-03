# main.py
import os
from dotenv import load_dotenv
from mistralai import Mistral
from dialogue_generator import generate_english_dialogue, extract_title, extract_dialogue_lines
from audio_generator import generate_audio_from_dialogue
from pdf_generator import generate_pdf_from_dialogue
from email_sender import send_email

def main():
    load_dotenv()
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    GMAIL_USER = os.getenv("GMAIL_USER")
    GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY manquante")
    if not GMAIL_USER or not GMAIL_PASSWORD:
        raise ValueError("GMAIL_USER ou GMAIL_PASSWORD manquant")
    print("✓ Configuration chargée")
    client = Mistral(api_key=MISTRAL_API_KEY)
    print("- Génération du dialogue...")
    dialogue = generate_english_dialogue(client)
    print("✓ Dialogue généré")
    title = extract_title(dialogue)
    if title:
        print(f"✓ Titre extrait : {title}")
    dialogue_lines = extract_dialogue_lines(dialogue)
    print(f"✓ {len(dialogue_lines)} répliques extraites")
    audio_file = None
    if dialogue_lines:
        audio_file = generate_audio_from_dialogue(dialogue_lines, "dialogue_anglais.mp3")
    pdf_file = generate_pdf_from_dialogue(dialogue, title, "dialogue_anglais.pdf")
    print("- Envoi de l'email...")
    send_email(GMAIL_USER, GMAIL_PASSWORD, dialogue, audio_file, pdf_file, title)
    print("✓ Email envoyé")
    if audio_file and os.path.exists(audio_file):
        os.remove(audio_file)
    if pdf_file and os.path.exists(pdf_file):
        os.remove(pdf_file)

if __name__ == "__main__":
    main()