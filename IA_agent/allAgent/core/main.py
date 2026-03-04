# core/main.py
# ============================================================
# Point d'entrée principal — fonctionne pour toutes les langues
# Usage : python core/main.py greek
#         python core/main.py italian
#         python core/main.py spanish
#         python core/main.py english
# ============================================================

import os
import sys
import importlib
from dotenv import load_dotenv
from mistralai import Mistral

# Permet les imports relatifs depuis la racine du projet
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from core.dialogue_generator import generate_dialogue, extract_title, extract_dialogue_lines
from core.audio_generator    import generate_audio
from core.pdf_generator      import generate_pdf
from core.email_sender       import send_email


def main():
    # ── Lecture de la langue en argument ────────────────────
    if len(sys.argv) < 2:
        print("Usage : python core/main.py <langue>")
        print("Langues disponibles : greek, italian, spanish, english")
        sys.exit(1)

    lang_code = sys.argv[1]

    # ── Chargement dynamique du fichier de langue ────────────
    try:
        lang = importlib.import_module(f"languages.{lang_code}")
    except ModuleNotFoundError:
        print(f"Erreur : langue '{lang_code}' introuvable dans languages/")
        sys.exit(1)

    # ── Variables d'environnement ────────────────────────────
    load_dotenv()
    API_KEY   = os.getenv("MISTRAL_API_KEY")
    GMAIL_USR = os.getenv("GMAIL_USER")
    GMAIL_PWD = os.getenv("GMAIL_PASSWORD")

    if not API_KEY:
        raise ValueError("MISTRAL_API_KEY manquante")
    if not GMAIL_USR or not GMAIL_PWD:
        raise ValueError("GMAIL_USER ou GMAIL_PASSWORD manquant")

    print(f"ok Config chargée — langue : {lang_code} | niveau : {lang.LEVEL} | vitesse : {lang.AUDIO_RATE}")
    print(f"   Destinataires : {', '.join(lang.EMAIL_RECIPIENTS)}")

    # ── Génération du dialogue ───────────────────────────────
    client = Mistral(api_key=API_KEY)
    print("- Génération du dialogue...")
    dialogue = generate_dialogue(client, lang)
    print("ok Dialogue généré")

    title = extract_title(dialogue)
    if title:
        print(f"ok Titre : {title}")

    lines = extract_dialogue_lines(dialogue, lang)
    print(f"ok {len(lines)} répliques extraites")

    # ── Audio ────────────────────────────────────────────────
    audio_file = None
    if lines:
        audio_file = generate_audio(lines, lang, f"{lang.OUTPUT_PREFIX}.mp3")

    # ── PDF ──────────────────────────────────────────────────
    pdf_file = generate_pdf(
        dialogue, lang, title, config,
        f"{lang.OUTPUT_PREFIX}.pdf"
    )

    # ── Email ────────────────────────────────────────────────
    print("- Envoi de l'email...")
    send_email(GMAIL_USR, GMAIL_PWD, dialogue, lang, title, audio_file, pdf_file)
    print("ok Email envoyé")

    # ── Nettoyage ────────────────────────────────────────────
    for f in [audio_file, pdf_file]:
        if f and os.path.exists(f):
            os.remove(f)
            print(f"ok Nettoyé : {f}")


if __name__ == "__main__":
    main()
