from flask import Flask, render_template, request, jsonify, session
from mistralai import Mistral
from dotenv import load_dotenv
import os
import secrets
import json
import re
import base64
import requests

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(16))

# Configuration Mistral
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Pour Whisper
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
    """Transcrire l'audio en texte avec Whisper sur Hugging Face"""
    try:
        if not HUGGINGFACE_API_KEY:
            return jsonify({
                'error': 'Hugging Face API key not configured',
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
        
        print(f"Audio size: {len(audio_bytes)} bytes")
        
        # Vérifier que l'audio n'est pas vide
        if len(audio_bytes) < 100:
            return jsonify({
                'error': 'Audio trop court ou vide',
                'success': False
            }), 400
        
        # Appeler l'API Hugging Face Inference
        # Essayer plusieurs modèles Whisper dans l'ordre de préférence
        models = [
            "openai/whisper-large-v3-turbo",
            "openai/whisper-medium",
            "openai/whisper-small",
        ]
        
        result = None
        used_model = None
        last_error = None
        
        for model in models:
            API_URL = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
            
            print(f"Trying model: {model}")
            try:
                response = requests.post(API_URL, headers=headers, data=audio_bytes, timeout=30)
                
                print(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    used_model = model
                    print(f"Success with model: {model}")
                    break
                elif response.status_code == 503:
                    # Modèle en cours de chargement, continuer vers le suivant
                    print(f"Model {model} is loading, trying next...")
                    continue
                else:
                    print(f"Model {model} returned status {response.status_code}: {response.text[:200]}")
                    last_error = response.text
                    continue
                    
            except Exception as e:
                print(f"Error with model {model}: {e}")
                last_error = str(e)
                continue
        
        if not used_model:
            return jsonify({
                'error': 'Aucun modèle Whisper disponible',
                'details': last_error,
                'success': False
            }), 503
        
        print(f"Response text: {response.text[:500]}")  # Premiers 500 caractères
        
        # Vérifier le statut HTTP
        if response.status_code != 200:
            return jsonify({
                'error': f'Erreur API Hugging Face (status {response.status_code})',
                'details': response.text[:200],
                'success': False
            }), response.status_code
        
        # Parser la réponse JSON
        try:
            result = response.json()
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Raw response: {response.text}")
            return jsonify({
                'error': 'Réponse invalide de Hugging Face',
                'details': response.text[:200],
                'success': False
            }), 500
        
        # Vérifier si le modèle charge
        if isinstance(result, dict) and 'error' in result:
            error_msg = result['error']
            if 'loading' in error_msg.lower() or 'currently loading' in error_msg.lower():
                return jsonify({
                    'error': 'Le modèle se charge, réessayez dans 20 secondes',
                    'success': False,
                    'loading': True
                }), 503
            
            print(f"Hugging Face error: {result}")
            return jsonify({
                'error': error_msg,
                'success': False
            }), 500
        
        # Extraire le texte transcrit
        text = result.get('text', '') if isinstance(result, dict) else ''
        
        if not text:
            print(f"No text in result: {result}")
            return jsonify({
                'error': 'Aucun texte transcrit',
                'success': False
            }), 500
        
        print(f"Transcribed text: {text}")
        
        return jsonify({
            'text': text.strip(),
            'success': True
        })
        
    except requests.Timeout:
        return jsonify({
            'error': 'Timeout - le serveur Hugging Face ne répond pas',
            'success': False
        }), 504
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