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

# Configuration de ffmpeg pour Windows (si nécessaire)
# Décommenter et ajuster le chemin si ffmpeg n'est pas dans le PATH
# AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
# AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

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

print(f"- API Key chargée ...")

# Initialiser le client Mistral
client = Mistral(api_key=MISTRAL_API_KEY)

def generate_greek_dialogue():
    prompt = """
    Crée un dialogue en grec moderne (niveau C1) entre Stephanos et Anna, sur le sujet suivant : {sujet}
    
    Le dialogue doit faire environ une page A4 (environ 500 mots).
    
    FORMATAGE DU DIALOGUE :
    - Commence par un titre en grec en rapport avec le sujet du dialogue, au format : <h3>Titre en grec</h3>
    - Exemple : <h3>Στο Σουπερμάρκετ</h3> ou <h3>Μια Συζήτηση για τον Καιρό</h3>
    - Ensuite, chaque réplique doit être dans une balise <p> séparée
    - Format : <p><strong>Nom du personnage :</strong> texte de la réplique</p>
    - Exemple : <p><strong>Στέφανος:</strong> Γεια σου Άννα! Τι κάνεις;</p>
    - Chaque réplique dans son propre paragraphe <p> pour créer un retour à la ligne automatique
    
    VOCABULAIRE :
    Après le dialogue, ajoute une section "Λεξιλόγιο" (Vocabulaire) avec un tableau HTML.
    
    Le tableau doit avoir 3 colonnes :
    - Colonne 1 : Mot en grec (en gras)
    - Colonne 2 : Traduction en français
    - Colonne 3 : Phrase d'exemple en grec
    
    Utilise ce format de tableau :
    <table class="vocab-table">
        <thead>
            <tr>
                <th>Grec</th>
                <th>Français</th>
                <th>Exemple</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>mot grec</strong></td>
                <td>traduction</td>
                <td>phrase d'exemple</td>
            </tr>
        </tbody>
    </table>
    
    Assure-toi que le vocabulaire contient environ 20-25 mots clés du dialogue.
    """
    
    # Liste de sujets
    sujets = [
        "Les courses au marché", "Un dîner en famille",
        "Une sortie au cinéma", "Un problème de voisinage",
        "Un voyage en bus", "Une discussion sur la météo", "Les plans pour le week-end",
        "Une visite chez le médecin", "L'organisation d'une fête", "Une conversation au café",
        "Les activités de loisirs", "Une dispute amicale", "Les traditions grecques",
        "Une journée à la plage", "Les transports en commun", "les voyages en bateau"
        "Une rencontre imprévue", "Les habitudes alimentaires",
        "Les projets de vacances", "Une visite culturelle", "la littérature grecque", 
        "la Crète", "Chios", "Samos", "Athènes", "Thessalonique", "Les îles grecques",
        "La Thessalie", "les séries grecques populaires", "le cinéma grec", "la musique grecque contemporaine"
        "le rébétiko", "la cuisine grecque traditionnelle", "les sites archéologiques en Grèce",
        "les musées archéologiques", "l'histoire de la Grèce antique", "la mythologie grecque",
        "les fêtes religieuses en Grèce", "la guerre d'indépendance grecque",
        "la vie quotidienne en Grèce moderne", "l'histoire moderne de la Grèce", "la politique en Grèce contemporaine"
        "les grands philosophes grecs", "la démocratie athénienne", "les Jeux Olympiques antiques",
        "la philosophie stoïcienne", "les écoles philosophiques grecques", "la statuaire grecque antique",
        "un rapprochement amoureux", "une discussion de séduction", "une conversation sur les relations amoureuses"

    ]
    
    sujet = sujets[datetime.now().day % len(sujets)]
    
    # Utilisation de la méthode chat.complete
    chat_response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt.format(sujet=sujet)}]
    )
    
    return chat_response.choices[0].message.content

def extract_title(html_content):
    """
    Extrait le titre du dialogue depuis la balise <h3>
    """
    title_pattern = r'<h3>(.*?)</h3>'
    match = re.search(title_pattern, html_content, re.IGNORECASE | re.DOTALL)
    
    if match:
        title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        return title
    
    return None

def extract_dialogue_lines(html_content):
    """
    Extrait les répliques du dialogue HTML et retourne une liste de tuples (speaker, text)
    """
    dialogue_lines = []
    
    # Pattern pour extraire les répliques : <p><strong>Nom:</strong> texte</p>
    pattern = r'<p><strong>(Στέφανος|Άννα):</strong>\s*(.*?)</p>'
    matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
    
    for speaker, text in matches:
        # Nettoyer le texte des balises HTML résiduelles
        clean_text = re.sub(r'<[^>]+>', '', text).strip()
        
        # Normaliser les noms pour la comparaison
        speaker_normalized = "Stephanos" if "Στέφανος" in speaker else "Anna"
        
        dialogue_lines.append((speaker_normalized, clean_text))
    
    return dialogue_lines

def generate_audio_from_dialogue(dialogue_lines, output_file="dialogue.mp3"):
    """
    Génère un fichier audio MP3 à partir des répliques du dialogue
    avec des voix différenciées pour Stephanos (homme) et Anna (femme)
    """
    if not dialogue_lines:
        print("⚠️  Aucune réplique trouvée dans le dialogue")
        return None
    
    print(f"- Génération audio de {len(dialogue_lines)} répliques...")
    audio_segments = []
    
    # Créer un dossier temporaire pour les fichiers audio
    with tempfile.TemporaryDirectory() as temp_dir:
        for i, (speaker, text) in enumerate(dialogue_lines):
            try:
                # Générer l'audio avec gTTS (langue grecque)
                tts = gTTS(text=text, lang='el', slow=False)
                
                # Sauvegarder temporairement
                temp_file = os.path.join(temp_dir, f"temp_{i}_{speaker}.mp3")
                tts.save(temp_file)
                
                # Charger avec pydub
                audio = AudioSegment.from_mp3(temp_file)
                
                # Ajuster la tonalité (pitch) pour différencier les voix
                if speaker == "Stephanos":
                    # Voix plus grave pour l'homme (-10% de fréquence)
                    audio = audio._spawn(audio.raw_data, overrides={
                        "frame_rate": int(audio.frame_rate * 0.9)
                    }).set_frame_rate(audio.frame_rate)
                else:  # Anna
                    # Voix plus aiguë pour la femme (+10% de fréquence)
                    audio = audio._spawn(audio.raw_data, overrides={
                        "frame_rate": int(audio.frame_rate * 1.1)
                    }).set_frame_rate(audio.frame_rate)
                
                # Ajouter l'audio
                audio_segments.append(audio)
                
                # Ajouter une pause entre les répliques (800ms)
                pause = AudioSegment.silent(duration=800)
                audio_segments.append(pause)
                
                print(f"  ✓ Réplique {i+1}/{len(dialogue_lines)} - {speaker}")
                
            except Exception as e:
                print(f"  ✗ Erreur pour la réplique {i+1}: {e}")
                continue
        
        if not audio_segments:
            print("⚠️  Aucun segment audio généré")
            return None
        
        # Combiner tous les segments
        print("- Assemblage des segments audio...")
        final_audio = sum(audio_segments)
        
        # Exporter le fichier final
        final_audio.export(output_file, format="mp3")
        print(f"✓ Audio généré : {output_file} ({len(final_audio)/1000:.1f}s)")
    
    return output_file

def generate_pdf_from_dialogue(html_content, title=None, output_file="dialogue_grec.pdf"):
    """
    Génère un fichier PDF stylisé à partir du dialogue HTML
    """
    print(f"- Génération du PDF...")
    
    # Titre du document
    pdf_title = title if title else "Dialogue en grec moderne"
    
    # Template HTML complet pour le PDF
    pdf_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{pdf_title}</title>
        <style>
            @page {{
                size: A4;
                margin: 1.5cm;
            }}
            
            body {{
                font-family: 'Arial', 'Helvetica', sans-serif;
                line-height: 1.4;
                color: #333;
                font-size: 11pt;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 2px solid #3498db;
            }}
            
            .header h1 {{
                color: #2c3e50;
                font-size: 20px;
                margin: 5px 0;
            }}
            
            .header .date {{
                color: #7f8c8d;
                font-size: 11px;
            }}
            
            .dialogue {{
                background-color: #f9f9f9;
                padding: 12px;
                border-radius: 5px;
                margin-bottom: 15px;
            }}
            
            .dialogue h3 {{
                color: #34495e;
                margin-top: 0;
                margin-bottom: 12px;
                font-size: 16px;
            }}
            
            .dialogue p {{
                margin: 6px 0;
                font-size: 11pt;
            }}
            
            .dialogue strong {{
                color: #2c3e50;
                font-weight: bold;
            }}
            
            .vocab-section {{
                margin-top: 15px;
            }}
            
            .vocab-section h3 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 5px;
                font-size: 16px;
                margin-bottom: 10px;
            }}
            
            .vocab-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                font-size: 11pt;
            }}
            
            .vocab-table th {{
                background-color: #3498db;
                color: white;
                padding: 4px 4px;
                text-align: left;
                font-weight: bold;
                font-size: 11pt;
            }}
            
            .vocab-table td {{
                border: 1px solid #ddd;
                padding: 3px 4px;
                vertical-align: top;
                line-height: 1.3;
            }}
            
            .vocab-table tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            
            .vocab-table td:first-child {{
                font-weight: bold;
                color: #2c3e50;
                width: 18%;
            }}
            
            .vocab-table td:nth-child(2) {{
                width: 22%;
            }}
            
            .vocab-table td:nth-child(3) {{
                width: 60%;
            }}
            
            .footer {{
                margin-top: 20px;
                padding-top: 10px;
                border-top: 1px solid #ecf0f1;
                text-align: center;
                color: #7f8c8d;
                font-size: 11pt;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{pdf_title}</h1>
            <div class="date">{datetime.now().strftime('%d/%m/%Y')}</div>
        </div>
        
        <div class="dialogue">
            {html_content}
        </div>
    </body>
    </html>
    """
    
    try:
        # Générer le PDF avec WeasyPrint
        HTML(string=pdf_html).write_pdf(output_file)
        
        file_size = os.path.getsize(output_file) / 1024  # Taille en KB
        print(f"✓ PDF généré : {output_file} ({file_size:.1f} KB)")
        return output_file
    
    except Exception as e:
        print(f"⚠️  Erreur lors de la génération du PDF : {e}")
        return None

def send_email(content, audio_file=None, pdf_file=None, title=None):
    # Liste des destinataires
    recipients = ["eminet666@gmail.com", "anne.lafond@ensaama.net"]
    
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = ", ".join(recipients)
    
    # Créer le subject avec le titre si disponible
    if title:
        msg["Subject"] = f"🎧 {title} - Dialogue grec quotidien"
    else:
        msg["Subject"] = "Ton dialogue grec quotidien 🎧"
    
    # Titre pour l'en-tête de l'email
    email_title = f"{title}" if title else "Dialogue en grec moderne"
    
    # Message d'information sur les pièces jointes
    attachments_info = []
    if audio_file:
        attachments_info.append("🎧 Fichier audio pour améliorer ta prononciation")
    if pdf_file:
        attachments_info.append("📄 PDF à imprimer ou à conserver")
    
    attachments_html = ""
    if attachments_info:
        attachments_html = f"""
        <div class="audio-notice">
            <strong>Pièces jointes incluses :</strong><br>
            {'<br>'.join(attachments_info)}
        </div>
        """
    
    # Utilisation de HTML pour un meilleur affichage dans l'email
    html_content = f"""
    <html>
        <head>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    line-height: 1.5; 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 15px;
                    font-size: 14px;
                }}
                h2 {{ 
                    color: #2c3e50; 
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 8px;
                    margin-bottom: 12px;
                    font-size: 20px;
                }}
                h3 {{
                    color: #34495e;
                    margin-top: 15px;
                    margin-bottom: 10px;
                    font-size: 16px;
                }}
                .audio-notice {{
                    background-color: #e8f4f8;
                    padding: 10px;
                    border-radius: 4px;
                    margin: 12px 0;
                    font-size: 12px;
                }}
                .dialogue {{ 
                    background-color: #f9f9f9; 
                    padding: 12px; 
                    border-radius: 5px;
                }}
                .dialogue p {{
                    margin: 6px 0;
                }}
                .vocab-table {{ 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin-top: 12px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    font-size: 14px;
                }}
                .vocab-table th {{ 
                    background-color: #3498db; 
                    color: white;
                    padding: 5px 4px;
                    text-align: left;
                    font-weight: bold;
                    font-size: 14px;
                }}
                .vocab-table td {{ 
                    border: 1px solid #ddd; 
                    padding: 4px 5px; 
                    text-align: left; 
                    vertical-align: top;
                    line-height: 1.3;
                }}
                .vocab-table tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                .vocab-table tr:hover {{
                    background-color: #e8f4f8;
                }}
                .vocab-table td:first-child {{
                    width: 18%;
                }}
                .vocab-table td:nth-child(2) {{
                    width: 22%;
                }}
                .vocab-table td:nth-child(3) {{
                    width: 60%;
                }}
            </style>
        </head>
        <body>
            <h2>{email_title}</h2>
            <div class="dialogue">
                {content}
            </div>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    
    # Ajouter le fichier audio en pièce jointe si disponible
    if audio_file and os.path.exists(audio_file):
        try:
            with open(audio_file, "rb") as attachment:
                part = MIMEBase("audio", "mpeg")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            # Ajouter un nom de fichier avec la date
            filename = f"dialogue_grec_{datetime.now().strftime('%Y%m%d')}.mp3"
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            
            msg.attach(part)
            print(f"✓ Fichier audio attaché : {filename}")
        except Exception as e:
            print(f"⚠️  Erreur lors de l'attachement du fichier audio : {e}")
    
    # Ajouter le fichier PDF en pièce jointe si disponible
    if pdf_file and os.path.exists(pdf_file):
        try:
            with open(pdf_file, "rb") as attachment:
                part = MIMEBase("application", "pdf")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            # Ajouter un nom de fichier avec la date
            filename = f"dialogue_grec_{datetime.now().strftime('%Y%m%d')}.pdf"
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            
            msg.attach(part)
            print(f"✓ Fichier PDF attaché : {filename}")
        except Exception as e:
            print(f"⚠️  Erreur lors de l'attachement du fichier PDF : {e}")
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    # Générer le dialogue
    dialogue = generate_greek_dialogue()
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
    send_email(dialogue, audio_file, pdf_file, title)
    print(f"✓ Email envoyé avec audio et PDF en pièces jointes")
    
    # Nettoyer les fichiers locaux
    if audio_file and os.path.exists(audio_file):
        os.remove(audio_file)
        print(f"✓ Fichier audio local nettoyé")
    
    if pdf_file and os.path.exists(pdf_file):
        os.remove(pdf_file)
        print(f"✓ Fichier PDF local nettoyé")