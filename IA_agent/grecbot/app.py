from flask import Flask, render_template, request, jsonify, session
from mistralai import Mistral
from dotenv import load_dotenv
import os
import secrets
import json
import re
import base64
import requests
import tempfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(16))

# Configuration Mistral
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "mistral-large-latest"

# Configuration email (Gmail)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "eminet666@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Prompt système
SYSTEM_PROMPT = """Είσαι ένας φιλικός βοηθός που μιλάει ελληνικά. 
Στόχος σου είναι να κάνεις φυσικές συνομιλίες στα νέα ελληνικά.
Ο συνομιλητής σου έχει επίπεδο C1 στα ελληνικά, οπότε μπορείς να χρησιμοποιείς:
- Σύνθετο λεξιλόγιο και ιδιωματισμούς
- Αποχρώσεις και λεπτές διακρίσεις στη γλώσσα
- Πολιτιστικές αναφορές και σύγχρονες εκφράσεις
- Διάφορα μητρώα γλώσσας (επίσημο, ανεπίσημο)
Απάντα πάντα στα ελληνικά με φυσικό και ευφράδη τρόπο, όπως θα μιλούσες με έναν προχωρημένο μαθητή.
ΣΗΜΑΝΤΙΚΟ: Μην χρησιμοποιείς ποτέ emoji ή emoticons στις απαντήσεις σου, ούτε στο κείμενο ούτε στο JSON.

CRITICAL: Your response MUST be valid JSON with this exact structure:
{
  "text": "your full Greek response here",
  "vocabulary": [
    {"word": "Greek word", "translation": "French translation in context"},
    {"word": "another word", "translation": "its translation"}
  ]
}

Rules for vocabulary:
- Select maximum 10 complex/advanced words from your response
- Choose words that are C1 level or challenging
- Provide contextual French translation (not dictionary definition)
- Return ONLY valid JSON, no markdown, no preamble, no explanation
- NO emojis or emoticons anywhere in the JSON"""

@app.route('/')
def index():
    """Page d'accueil"""
    session.clear()
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint pour les messages de chat"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message vide'}), 400
        
        if 'history' not in session:
            session['history'] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
        
        history = session['history']
        history.append({"role": "user", "content": user_message})
        
        client = Mistral(api_key=MISTRAL_API_KEY)
        response = client.chat.complete(
            model=MODEL,
            messages=history
        )
        
        assistant_message = response.choices[0].message.content
        
        cleaned = assistant_message.strip()
        if cleaned.startswith('```json'):
            cleaned = re.sub(r'^```json\s*', '', cleaned)
            cleaned = re.sub(r'\s*```$', '', cleaned)
        elif cleaned.startswith('```'):
            cleaned = re.sub(r'^```\s*', '', cleaned)
            cleaned = re.sub(r'\s*```$', '', cleaned)
        
        try:
            parsed = json.loads(cleaned)
            text = parsed.get('text', '').strip()
            vocabulary = parsed.get('vocabulary', [])
            
            text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            text = re.sub(r'\s+', ' ', text)
            
            for item in vocabulary:
                if 'translation' in item:
                    item['translation'] = item['translation'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                    item['translation'] = re.sub(r'\s+', ' ', item['translation']).strip()
                if 'word' in item:
                    item['word'] = item['word'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                    item['word'] = re.sub(r'\s+', ' ', item['word']).strip()
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {assistant_message}")
            text = assistant_message.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            text = re.sub(r'\s+', ' ', text)
            vocabulary = []
        
        history.append({"role": "assistant", "content": text})
        
        if len(history) > 52:
            history = [history[0]] + history[-50:]
        
        session['history'] = history
        
        return jsonify({
            'response': text,
            'vocabulary': vocabulary,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/reset', methods=['POST'])
def reset():
    """Réinitialiser la conversation"""
    session.clear()
    return jsonify({'success': True, 'message': 'Conversation réinitialisée'})

@app.route('/translate', methods=['POST'])
def translate():
    """Traduire un texte grec en français"""
    try:
        data = request.json
        greek_text = data.get('text', '').strip()
        
        if not greek_text:
            return jsonify({'error': 'Texte vide'}), 400
        
        translation_prompt = f"""Traduis ce texte grec en français de manière naturelle et précise:

{greek_text}

Donne uniquement la traduction en français, sans explications supplémentaires."""
        
        client = Mistral(api_key=MISTRAL_API_KEY)
        response = client.chat.complete(
            model=MODEL,
            messages=[{"role": "user", "content": translation_prompt}]
        )
        
        translation = response.choices[0].message.content
        
        return jsonify({
            'translation': translation,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/enrich-vocabulary', methods=['POST'])
def enrich_vocabulary():
    """Enrichir le vocabulaire avec exemples et formes verbales"""
    try:
        data = request.json
        words = data.get('words', [])
        
        if not words:
            return jsonify({'words': [], 'success': True})
        
        words_list = ', '.join([f'"{w}"' for w in words])
        
        prompt = f"""Pour chaque mot grec suivant: {words_list}

Fournis UNIQUEMENT un JSON valide avec cette structure exacte:
{{
  "words": [
    {{
      "word": "mot grec",
      "translation": "traduction française",
      "example": "exemple d'usage en grec",
      "example_translation": "traduction de l'exemple",
      "verb_forms": "présent: X, aoriste: Y" (seulement si c'est un verbe, sinon null)
    }}
  ]
}}

IMPORTANT:
- Si le mot est un VERBE, donne les formes: présent (1ère personne singulier) et aoriste
- Si ce n'est PAS un verbe, mets verb_forms: null
- L'exemple doit être une phrase courte et naturelle
- Retourne UNIQUEMENT le JSON, sans markdown, sans explication"""

        client = Mistral(api_key=MISTRAL_API_KEY)
        response = client.chat.complete(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.choices[0].message.content.strip()
        
        if result.startswith('```json'):
            result = re.sub(r'^```json\s*', '', result)
            result = re.sub(r'\s*```$', '', result)
        elif result.startswith('```'):
            result = re.sub(r'^```\s*', '', result)
            result = re.sub(r'\s*```$', '', result)
        
        enriched = json.loads(result)
        
        return jsonify({
            'words': enriched.get('words', []),
            'success': True
        })
        
    except Exception as e:
        print(f"Enrichment error: {e}")
        return jsonify({
            'words': [],
            'success': False,
            'error': str(e)
        }), 500

@app.route('/send-pdf-email', methods=['POST'])
def send_pdf_email():
    """Envoyer le PDF par email"""
    
    try:
        # Vérifier la configuration email
        if not EMAIL_PASSWORD:
            print("⚠️ EMAIL_PASSWORD non configuré")
            return jsonify({
                'error': 'Configuration email manquante.',
                'success': False
            }), 400
        
        data = request.json
        pdf_data = data.get('pdf', '')
        dialogue = data.get('dialogue', '')
        recipient = data.get('email', EMAIL_ADDRESS)
        
        if not pdf_data:
            return jsonify({'error': 'Pas de données PDF'}), 400
        
        print(f"📧 Tentative d'envoi email à {recipient}")
        print(f"📦 Taille données PDF: {len(pdf_data)} caractères")
        
        if ',' in pdf_data:
            pdf_data = pdf_data.split(',')[1]
        
        pdf_bytes = base64.b64decode(pdf_data)
        print(f"✅ PDF décodé: {len(pdf_bytes)} bytes ({len(pdf_bytes)/1024:.2f} KB)")
        
        # Vérifier la taille
        if len(pdf_bytes) > 25 * 1024 * 1024:  # 25 MB limite Gmail
            return jsonify({
                'error': 'PDF trop volumineux (> 25 MB).',
                'success': False
            }), 413
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = f'Conversation Σωκράτης 2.0 - {datetime.now().strftime("%Y-%m-%d")}'
        
        # Corps de l'email avec le dialogue
        body = f"""Bonjour,

Voici votre conversation avec Σωκράτης 2.0.

═══════════════════════════════════════
DIALOGUE DE LA SESSION
═══════════════════════════════════════
{dialogue}

═══════════════════════════════════════

Le PDF en pièce jointe contient la conversation complète avec le vocabulaire enrichi (exemples d'usage et conjugaisons).

Καλή συνέχεια!

---
Σωκράτης 2.0 Bot
"""
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        filename = f'Socrate_{datetime.now().strftime("%Y-%m-%d")}.pdf'
        attachment = MIMEBase('application', 'pdf')
        attachment.set_payload(pdf_bytes)
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(attachment)
        
        print(f"📨 Connexion à Gmail SMTP...")
        
        # Augmenter le timeout SMTP
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=60) as server:
            server.starttls()
            print(f"🔐 Authentification...")
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print(f"✉️ Envoi du message...")
            server.send_message(msg)
        
        print(f"✅ Email envoyé avec succès!")
        return jsonify({
            'success': True,
            'message': f'Email envoyé à {recipient}'
        })
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = "Erreur d'authentification Gmail. Vérifiez le mot de passe d'application."
        print(f"❌ {error_msg}: {e}")
        return jsonify({
            'error': error_msg,
            'success': False
        }), 401
    
    except smtplib.SMTPException as e:
        error_msg = f"Erreur SMTP: {str(e)}"
        print(f"❌ {error_msg}")
        return jsonify({
            'error': error_msg,
            'success': False
        }), 500
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erreur email: {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': error_msg,
            'success': False
        }), 500

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Transcrire l'audio en texte avec Whisper sur Groq"""
    try:
        if not GROQ_API_KEY:
            return jsonify({
                'error': 'Groq API key not configured',
                'success': False
            }), 500
        
        data = request.json
        audio_data = data.get('audio', '')
        
        if not audio_data:
            return jsonify({'error': 'Pas de données audio'}), 400
        
        if ',' in audio_data:
            audio_data = audio_data.split(',')[1]
        
        audio_bytes = base64.b64decode(audio_data)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name
        
        try:
            url = "https://api.groq.com/openai/v1/audio/transcriptions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}"
            }
            
            with open(temp_path, 'rb') as audio_file:
                files = {
                    'file': ('audio.webm', audio_file, 'audio/webm'),
                    'model': (None, 'whisper-large-v3'),
                    'language': (None, 'el')
                }
                
                response = requests.post(url, headers=headers, files=files)
                result = response.json()
            
            if 'error' in result:
                print(f"Groq error: {result}")
                return jsonify({
                    'error': result.get('error', {}).get('message', 'Erreur inconnue'),
                    'success': False
                }), 500
            
            text = result.get('text', '')
            
            return jsonify({
                'text': text.strip(),
                'success': True
            })
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        print(f"Transcription error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

if __name__ == '__main__':
    if not MISTRAL_API_KEY:
        print("⚠️  ERREUR: MISTRAL_API_KEY non trouvée!")
        exit(1)
    
    app.run(debug=True, host='0.0.0.0', port=5000)