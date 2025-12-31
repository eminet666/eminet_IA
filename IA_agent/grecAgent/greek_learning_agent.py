import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from mistralai import Mistral
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment
from pydub.utils import which
import re
import tempfile
from weasyprint import HTML, CSS
from io import BytesIO

# CHARGEMENT .env
load_dotenv()
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
SPEED = float(os.getenv('SPEED', 0.8))  # 🔥 NOUVEAU : Vitesse 0.8x

print("🚀 API Key chargée...")
print(f"🔊 Vitesse TTS: {SPEED}x")

# VÉRIFICATION CLÉS
if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY n'est pas définie dans les variables d'environnement")
if not GMAIL_USER or not GMAIL_PASSWORD:
    raise ValueError("GMAIL_USER ou GMAIL_PASSWORD manquant")
print("- Vérification des clés OK")

client = Mistral(api_key=MISTRAL_API_KEY)

def generategreekdialogue(sujet):
    """Génère dialogue grec B2 avec Mistral"""
    prompt = f"""Crée un dialogue en grec moderne niveau B2 entre Stephanos et Anna, sur le sujet suivant : {sujet}

Le dialogue doit faire environ une page A4 (~500 mots).

FORMATAGE DU DIALOGUE :
- Commence par un titre en grec en rapport avec le sujet du dialogue, au format <h3>Titre en grec</h3>
- Exemple : <h3>Οι αγορές στην αγορά</h3> ou <h3>Ένα δείπνο με την οικογένεια</h3>
- Ensuite, chaque réplique doit être dans une balise <p> séparée
- Format : <p><strong>Nom du personnage</strong> : texte de la réplique</p>
- Exemple : <p><strong>Στέφανος</strong> : Γεια σου Άννα!</p>
- Chaque réplique dans son propre paragraphe <p> pour créer un retour à la ligne automatique

VOCABULAIRE : Après le dialogue, ajoute une section "Λεξιλόγιο" avec un tableau HTML.
Le tableau doit avoir 3 colonnes :
- Colonne 1 : Mot en grec (en gras)
- Colonne 2 : Traduction en français  
- Colonne 3 : Phrase d'exemple en grec

Utilise ce format de tableau :
<table class="vocab-table">
<thead>
<tr><th>Ελληνικά</th><th>Français</th><th>Παράδειγμα</th></tr>
</thead>
<tbody>
<tr><td><strong>αγορά</strong></td><td>marché</td><td>Πάω στην αγορά κάθε Σάββατο.</td></tr>
</tbody>
</table>

Assure-toi que le vocabulaire contient environ 20-25 mots clés du dialogue."""

    print("🤖 Utilisation de la méthode chat.complete...")
    chatresponse = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt.format(sujet=sujet)}]
    )
    return chatresponse.choices[0].message.content

def extracttitle(htmlcontent):
    """Extrait le titre du dialogue depuis la balise h3"""
    title_pattern = r'<h3>(.*?)</h3>'
    match = re.search(title_pattern, htmlcontent, re.IGNORECASE | re.DOTALL)
    if match:
        title = re.sub(r'<.*?>', '', match.group(1)).strip()
        return title
    return None

def extractdialoguelines(htmlcontent):
    """Extrait les répliques du dialogue HTML et retourne une liste de tuples (speaker, text)"""
    dialoguelines = []
    # Pattern pour extraire les répliques : <p><strong>Nom</strong> : texte</p>
    pattern = r'<p><strong>([^<]+)</strong>\s*:?\s*(.*?)</p>'
    matches = re.findall(pattern, htmlcontent, re.IGNORECASE | re.DOTALL)
    
    for speaker, text in matches:
        # Nettoyer le texte des balises HTML résiduelles
        cleantext = re.sub(r'<.*?>', '', text).strip()
        # Normaliser les noms pour la comparaison
        speakernormalized = "Stephanos" if "ΣΤΕΦΑΝΟΣ" in speaker.upper() or "ΣΤΕΦΑΝΟΣ" in speaker.upper() else "Anna"
        dialoguelines.append((speakernormalized, cleantext))
    
    return dialoguelines

def generateaudiofromdialogue(dialoguelines, outputfile="dialogue.mp3"):
    """🔥 gTTS AMÉLIORÉ : vitesse 0.8x + voix Anna/Stephanos différenciées"""
    if not dialoguelines:
        print("Aucune réplique trouvée dans le dialogue")
        return None
    
    print(f"- Génération gTTS amélioré ({len(dialoguelines)} répliques, {SPEED}x)...")
    audiosegments = []
    
    with tempfile.TemporaryDirectory() as tempdir:
        for i, (speaker, text) in enumerate(dialoguelines):
            try:
                # gTTS grec + slow=True (base ~0.8x)
                tts = gTTS(text=text, lang='el', slow=True)
                tempfile_path = os.path.join(tempdir, f"temp_{i}.mp3")
                tts.save(tempfile_path)
                
                audio = AudioSegment.from_mp3(tempfile_path)
                
                # 🔥 VOIX DIFFÉRENCIÉES (mieux que l'original)
                if speaker == "Stephanos":
                    # Masculin: voix GRAVE + lent
                    audio = audio._spawn(audio.raw_data, overrides={
                        "frame_rate": int(audio.frame_rate * 0.85)
                    }).set_frame_rate(audio.frame_rate)
                    audio = audio.speedup(playback_speed=0.92, chunk_size=150, crossfade=25)
                else:  # Anna
                    # Féminin: voix AIGUË + naturel
                    audio = audio._spawn(audio.raw_data, overrides={
                        "frame_rate": int(audio.frame_rate * 1.18)
                    }).set_frame_rate(audio.frame_rate)
                    audio = audio.speedup(playback_speed=1.02, chunk_size=150, crossfade=25)
                
                # 🔥 VITESSE FINALE 0.8x uniforme (configurable via .env)
                audio = audio.speedup(playback_speed=1/float(SPEED), chunk_size=200, crossfade=30)
                
                audiosegments.append(audio)
                
                # Pause 1s entre répliques (amélioré)
                pause = AudioSegment.silent(duration=1000)
                audiosegments.append(pause)
                
                print(f"  ✓ Réplique {i+1}/{len(dialoguelines)} - {speaker} ({len(text)} chars)")
                
            except Exception as e:
                print(f"  ✗ Erreur réplique {i+1} ({speaker}): {e}")
                continue
    
    if not audiosegments:
        print("Aucun segment audio généré")
        return None
    
    # Assemblage final
    print("- 🎵 Assemblage audio final...")
    final_audio = sum(audiosegments)
    final_audio.export(outputfile, format="mp3")
    duration = len(final_audio) / 1000
    print(f"✅ Audio prêt: {outputfile} ({duration:.1f}s)")
    return outputfile

def generatepdffromdialogue(htmlcontent, title=None, outputfile="dialoguegrec.pdf"):
    """Génère un fichier PDF stylisé partir du dialogue HTML"""
    print("- 📄 Génération du PDF...")
    pdftitle = title if title else "Dialogue en grec moderne"
    
    pdfhtml = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{pdftitle}</title>
    <style>
        @page {{ size: A4; margin: 1.5cm; }}
        body {{ font-family: Arial, Helvetica, sans-serif; line-height: 1.4; color: #333; font-size: 11pt; }}
        .header {{ text-align: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #3498db; }}
        .header h1 {{ color: #2c3e50; font-size: 20px; margin: 5px 0; }}
        .header .date {{ color: #7f8c8d; font-size: 11px; }}
        .dialogue {{ background-color: #f9f9f9; padding: 12px; border-radius: 5px; margin-bottom: 15px; }}
        .dialogue h3 {{ color: #34495e; margin-top: 0; margin-bottom: 12px; font-size: 16px; }}
        .dialogue p {{ margin: 6px 0; font-size: 11pt; }}
        .dialogue strong {{ color: #2c3e50; font-weight: bold; }}
        .vocab-section {{ margin-top: 15px; }}
        .vocab-section h3 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; font-size: 16px; margin-bottom: 10px; }}
        .vocab-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 11pt; }}
        .vocab-table th {{ background-color: #3498db; color: white; padding: 4px 4px; text-align: left; font-weight: bold; font-size: 11pt; }}
        .vocab-table td {{ border: 1px solid #ddd; padding: 3px 4px; vertical-align: top; line-height: 1.3; }}
        .vocab-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .vocab-table td:first-child {{ font-weight: bold; color: #2c3e50; width: 18%; }}
        .vocab-table td:nth-child(2) {{ width: 22%; }}
        .vocab-table td:nth-child(3) {{ width: 60%; }}
        .footer {{ margin-top: 20px; padding-top: 10px; border-top: 1px solid #ecf0f1; text-align: center; color: #7f8c8d; font-size: 11pt; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{pdftitle}</h1>
        <div class="date">{datetime.now().strftime('%d/%m/%Y')}</div>
    </div>
    <div class="dialogue">
        {htmlcontent}
    </div>
</body>
</html>"""
    
    try:
        HTML(string=pdfhtml).write_pdf(outputfile)
        filesize = os.path.getsize(outputfile) / 1024
        print(f"✅ PDF généré: {outputfile} ({filesize:.1f} KB)")
        return outputfile
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF: {e}")
        return None

def sendemail(content, audiofile=None, pdffile=None, title=None):
    """Envoie l'email avec les pièces jointes"""
    recipients = ["eminet666@gmail.com", "anne.lafond@ensaama.net"]
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = ", ".join(recipients)
    
    if title:
        msg['Subject'] = f"{title} - Dialogue grec quotidien"
    else:
        msg['Subject'] = "Ton dialogue grec quotidien"
    
    emailtitle = f"{title}" if title else "Dialogue en grec moderne"
    
    attachmentsinfo = []
    if audiofile:
        attachmentsinfo.append("Fichier audio 🎵 (pour améliorer ta prononciation)")
    if pdffile:
        attachmentsinfo.append("PDF 📄 (à imprimer ou conserver)")
    
    attachmentshtml = ""
    if attachmentsinfo:
        attachmentshtml = f"""
        <div class="audio-notice">
            <strong>Pièces jointes incluses :</strong><br><br>
            {'<br>'.join(attachmentsinfo)}
        </div>"""
    
    htmlcontent = f"""<html>
<head>
<style>
    body {{ font-family: Arial, sans-serif; line-height: 1.5; max-width: 800px; margin: 0 auto; padding: 15px; font-size: 14px; }}
    h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8px; margin-bottom: 12px; font-size: 20px; }}
    h3 {{ color: #34495e; margin-top: 15px; margin-bottom: 10px; font-size: 16px; }}
    .audio-notice {{ background-color: #e8f4f8; padding: 10px; border-radius: 4px; margin: 12px 0; font-size: 12px; }}
    .dialogue {{ background-color: #f9f9f9; padding: 12px; border-radius: 5px; }}
    .dialogue p {{ margin: 6px 0; }}
    .vocab-table {{ border-collapse: collapse; width: 100%; margin-top: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); font-size: 14px; }}
    .vocab-table th {{ background-color: #3498db; color: white; padding: 5px 4px; text-align: left; font-weight: bold; font-size: 14px; }}
    .vocab-table td {{ border: 1px solid #ddd; padding: 4px 5px; text-align: left; vertical-align: top; line-height: 1.3; }}
    .vocab-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
    .vocab-table tr:hover {{ background-color: #e8f4f8; }}
    .vocab-table td:first-child {{ width: 18%; }}
    .vocab-table td:nth-child(2) {{ width: 22%; }}
    .vocab-table td:nth-child(3) {{ width: 60%; }}
</style>
</head>
<body>
    <h2>{emailtitle}</h2>
    {attachmentshtml}
    <div class="dialogue">
        {content}
    </div>
</body>
</html>"""
    
    msg.attach(MIMEText(htmlcontent, 'html', 'utf-8'))
    
    # Audio
    if audiofile and os.path.exists(audiofile):
        try:
            with open(audiofile, 'rb') as attachment:
                part = MIMEBase('audio', 'mpeg')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            filename = f"dialoguegrec_{datetime.now().strftime('%Y%m%d')}.mp3"
            part.add_header('Content-Disposition', f'attachment; filename= {filename}')
            msg.attach(part)
            print(f"📎 Fichier audio attaché: {filename}")
        except Exception as e:
            print(f"Erreur lors de l'attachement du fichier audio: {e}")
    
    # PDF
    if pdffile and os.path.exists(pdffile):
        try:
            with open(pdffile, 'rb') as attachment:
                part = MIMEBase('application', 'pdf')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            filename = f"dialoguegrec_{datetime.now().strftime('%Y%m%d')}.pdf"
            part.add_header('Content-Disposition', f'attachment; filename= {filename}')
            msg.attach(part)
            print(f"📎 Fichier PDF attaché: {filename}")
        except Exception as e:
            print(f"Erreur lors de l'attachement du fichier PDF: {e}")
    
    # ENVOI
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)
    print("📧 Email envoyé avec audio et PDF en pièces jointes!")

if __name__ == "__main__":
    # Sujets quotidiens
    sujets = [
        "Les courses au marché",
        "Un dîner en famille", 
        "Une sortie au cinéma",
        "Un problème de voisinage",
        "Un voyage en bus",
        "Une discussion sur la météo"
    ]
    sujet = sujets[datetime.now().day % len(sujets)]
    print(f"📖 Sujet du jour: {sujet}")
    
    # 1. GÉNÉRATION DIALOGUE
    dialogue = generategreekdialogue(sujet)
    print("✅ Dialogue généré")
    
    # 2. EXTRACTION TITRE
    title = extracttitle(dialogue)
    if title:
        print(f"📛 Titre extrait: {title}")
    
    # 3. EXTRACTION RÉPLIQUES
    dialoguelines = extractdialoguelines(dialogue)
    print(f"💬 {len(dialoguelines)} répliques extraites")
    
    # 4. AUDIO AMÉLIORÉ 🔥
    audiofile = None
    if dialoguelines:
        audiofile = generateaudiofromdialogue(dialoguelines, "dialoguegrec.mp3")
    
    # 5. PDF
    pdffile = generatepdffromdialogue(dialogue, title, "dialoguegrec.pdf")
    
    # 6. EMAIL
    sendemail(dialogue, audiofile, pdffile, title)
    print("🎉 MISSION TERMINÉE!")
    
    # Nettoyage
    if audiofile and os.path.exists(audiofile):
        os.remove(audiofile)
        print("🧹 Fichier audio local nettoyé")
    if pdffile and os.path.exists(pdffile):
        os.remove(pdffile)
        print("🧹 Fichier PDF local nettoyé")
