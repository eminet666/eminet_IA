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

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(16))

# Configuration Mistral
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Pour Whisper ultra-rapide
MODEL = "mistral-large-latest"

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
    session.clear()  # Nouvelle session
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint pour les messages de chat"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message vide'}), 400
        
        # Récupérer ou initialiser l'historique
        if 'history' not in session:
            session['history'] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
        
        history = session['history']
        
        # Ajouter le message utilisateur
        history.append({"role": "user", "content": user_message})
        
        # Appeler Mistral API
        client = Mistral(api_key=MISTRAL_API_KEY)
        response = client.chat.complete(
            model=MODEL,
            messages=history
        )
        
        # Extraire la réponse
        assistant_message = response.choices[0].message.content
        
        # Nettoyer la réponse (enlever markdown si présent)
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
            
            # Nettoyer complètement le texte de tous les caractères problématiques
            text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            # Supprimer les doubles espaces
            import re as re_module
            text = re_module.sub(r'\s+', ' ', text)
            
            # Nettoyer aussi les traductions du vocabulaire
            for item in vocabulary:
                if 'translation' in item:
                    item['translation'] = item['translation'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                    item['translation'] = re_module.sub(r'\s+', ' ', item['translation']).strip()
                if 'word' in item:
                    item['word'] = item['word'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                    item['word'] = re_module.sub(r'\s+', ' ', item['word']).strip()
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {assistant_message}")
            # Si le parsing échoue, utiliser le texte brut
            text = assistant_message.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            import re as re_module
            text = re_module.sub(r'\s+', ' ', text)
            vocabulary = []
        
        # Ajouter à l'historique (texte seulement, pas le JSON)
        history.append({"role": "assistant", "content": text})
        
        # Limiter l'historique
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
        
        # Créer un prompt de traduction
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

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Transcrire l'audio en texte avec Whisper sur Groq (ultra-rapide et gratuit)"""
    try:
        if not GROQ_API_KEY:
            return jsonify({
                'error': 'Groq API key not configured',
                'success': False
            }), 500
        
        # Récupérer l'audio en base64
        data = request.json
        audio_data = data.get('audio', '')
        
        if not audio_data:
            return jsonify({'error': 'Pas de données audio'}), 400
        
        # Décoder le base64
        if ',' in audio_data:
            audio_data = audio_data.split(',')[1]
        
        audio_bytes = base64.b64decode(audio_data)
        
        # Sauvegarder temporairement
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name
        
        try:
            # Appeler l'API Groq (compatible OpenAI)
            import requests
            
            # Groq utilise une API compatible OpenAI
            url = "https://api.groq.com/openai/v1/audio/transcriptions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}"
            }
            
            with open(temp_path, 'rb') as audio_file:
                files = {
                    'file': ('audio.webm', audio_file, 'audio/webm'),
                    'model': (None, 'whisper-large-v3'),
                    'language': (None, 'el')  # Grec
                }
                
                response = requests.post(url, headers=headers, files=files)
                result = response.json()
            
            if 'error' in result:
                print(f"Groq error: {result}")
                return jsonify({
                    'error': result.get('error', {}).get('message', 'Erreur inconnue'),
                    'success': False
                }), 500
            
            # Extraire le texte transcrit
            text = result.get('text', '')
            
            return jsonify({
                'text': text.strip(),
                'success': True
            })
            
        finally:
            # Nettoyer le fichier temporaire
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
        print("⚠️  ERREUR: MISTRAL_API_KEY non trouvée dans les variables d'environnement!")
        exit(1)
    
    # Pour le développement local
    app.run(debug=True, host='0.0.0.0', port=5000)