import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from mistralai import Mistral
from datetime import datetime
import edge_tts
import asyncio
import re

# Charger le fichier .env
load_dotenv()

# Charger les variables d'environnement
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

# Vérification des clés
if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY n'est pas définie")
if not GMAIL_USER or not GMAIL_PASSWORD:
    raise ValueError("GMAIL_USER ou GMAIL_PASSWORD manquant")

# Initialiser le client Mistral
client = Mistral(api_key=MISTRAL_API_KEY)

def generate_greek_dialogue():
    prompt = """
    Crée un dialogue en grec moderne (niveau B2) entre Stephanos et Anna, sur un sujet de la vie quotidienne en Grèce.
    Le dialogue doit faire environ une page A4 (environ 500 mots).
    
    FORMAT REQUIS :
    - Chaque réplique doit commencer par le nom du personnage suivi de " : "
    - Exemple : "Stephanos: Καλημέρα, Άννα!"
    - Exemple : "Anna: Γεια σου, Στέφανε!"
    
    À la fin, ajoute une section VOCABULAIRE avec les règles suivantes :
    
    RÈGLES POUR LE VOCABULAIRE :
    1. **Pas de doublons** : Chaque mot ne doit apparaître qu'une seule fois dans la liste
    2. **Format pour les verbes** : Présente-les sous la forme "présent_indicatif / aoriste"
       Exemple : "αγοράζω / αγόρασα" (acheter)
    3. **Format pour les autres mots** : mot grec → traduction française
    4. **Phrase d'exemple** : Pour chaque mot, donne une phrase d'exemple en grec avec sa traduction
    5. **Organisation** : Utilise des balises HTML (<strong>texte</strong>) et des listes (<ul><li>...</li></ul>)
    
    EXEMPLE DE FORMAT POUR LE VOCABULAIRE :
    
    <h3>Vocabulaire</h3>
    <ul>
        <li><strong>αγοράζω / αγόρασα</strong> (acheter)
            <br>Exemple : Αγόρασα φρούτα από την αγορά. (J'ai acheté des fruits au marché.)</li>
        <li><strong>η αγορά</strong> (le marché)
            <br>Exemple : Η αγορά είναι ανοιχτή κάθε Σάββατο. (Le marché est ouvert chaque samedi.)</li>
    </ul>
    
    Sujet : {sujet}
    """

    sujets = [
        "Les courses au marché", "Un dîner en famille",
        "Une sortie au cinéma", "Un problème de voisinage",
        "Un voyage en bus", "Une discussion sur la météo"
    ]
    sujet = sujets[datetime.now().day % len(sujets)]

    chat_response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt.format(sujet=sujet)}]
    )

    return chat_response.choices[0].message.content

async def generate_audio_with_voices(dialogue_text, speed_rate=0.8):
    """
    Génère un fichier audio avec des voix différentes pour chaque personnage
    speed_rate: vitesse de lecture (0.5 = très lent, 1.0 = normal, 2.0 = rapide)
    """
    # Extraire les répliques du dialogue
    lines = dialogue_text.split('\n')
    dialogue_lines = []
    
    for line in lines:
        # Chercher les lignes avec "Stephanos:" ou "Anna:"
        if 'Stephanos:' in line or 'Στέφανος:' in line:
            text = re.sub(r'^.*?:', '', line).strip()
            dialogue_lines.append(('stephanos', text))
        elif 'Anna:' in line or 'Άννα:' in line:
            text = re.sub(r'^.*?:', '', line).strip()
            dialogue_lines.append(('anna', text))
    
    # Configuration des voix
    voices = {
        'stephanos': 'el-GR-NestorasNeural',  # Voix masculine
        'anna': 'el-GR-AthinaNeural'          # Voix féminine
    }
    
    # Convertir le taux de vitesse en format SSML
    # rate: -50% à +100% (0.5 = -50%, 1.0 = 0%, 2.0 = +100%)
    rate_percent = f"{int((speed_rate - 1) * 100)}%"
    
    # Générer des fichiers audio temporaires
    temp_files = []
    for i, (speaker, text) in enumerate(dialogue_lines):
        if not text.strip():
            continue
            
        output_file = f"temp_audio_{i}.mp3"
        voice = voices[speaker]
        
        # Créer le texte SSML avec contrôle de vitesse
        ssml_text = f'<speak><prosody rate="{rate_percent}">{text}</prosody></speak>'
        
        communicate = edge_tts.Communicate(ssml_text, voice)
        await communicate.save(output_file)
        temp_files.append(output_file)
    
    # Fusionner tous les fichiers audio
    # Note: pour une fusion simple, on peut utiliser pydub
    try:
        from pydub import AudioSegment
        
        combined = AudioSegment.empty()
        for file in temp_files:
            audio = AudioSegment.from_mp3(file)
            combined += audio
            # Ajouter une pause de 500ms entre les répliques
            combined += AudioSegment.silent(duration=500)
        
        output_path = "dialogue_grec.mp3"
        combined.export(output_path, format="mp3")
        
        # Nettoyer les fichiers temporaires
        for file in temp_files:
            if os.path.exists(file):
                os.remove(file)
        
        return output_path
    except ImportError:
        # Si pydub n'est pas disponible, retourner juste le premier fichier
        print("pydub non installé, impossible de fusionner les audios")
        if temp_files:
            os.rename(temp_files[0], "dialogue_grec.mp3")
            return "dialogue_grec.mp3"
        return None

def send_email_with_audio(content, audio_file=None):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = "eminet666@gmail.com"
    msg["Subject"] = "Ton dialogue grec quotidien 🇬🇷"

    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                h2 {{ color: #2c3e50; }}
                .dialogue {{ background-color: #f9f9f9; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h2>Dialogue en grec moderne 🎧</h2>
            <p>📎 Le fichier audio est en pièce jointe (vitesse ralentie à 80%)</p>
            <div class="dialogue">
                {content}
            </div>
        </body>
    </html>
    """

    msg.attach(MIMEText(html_content, "html", "utf-8"))

    # Attacher le fichier audio
    if audio_file and os.path.exists(audio_file):
        with open(audio_file, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= dialogue_grec.mp3",
        )
        msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    dialogue = generate_greek_dialogue()
    
    # Générer l'audio avec des voix différentes et vitesse ralentie
    audio_file = asyncio.run(generate_audio_with_voices(dialogue, speed_rate=0.8))
    
    # Envoyer l'email avec l'audio en pièce jointe
    send_email_with_audio(dialogue, audio_file)
    
    # Nettoyer le fichier audio
    if audio_file and os.path.exists(audio_file):
        os.remove(audio_file)