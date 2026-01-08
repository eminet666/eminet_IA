"""
Application Flask - Σωκράτης 2.0
Chatbot pour l'apprentissage du grec moderne (niveau C1)

Architecture intermédiaire : 
- app.py : Routes + logique (ce fichier)
- config.py : Configuration
- prompts.py : Prompts système
- services.py : Services (Mistral, Groq, Email, Azure Speech)
"""
from flask import Flask, render_template, request, jsonify, session
import json
import re
import base64
import sys
from config import Config
from prompts import get_system_prompt, TRANSLATION_PROMPT_TEMPLATE, VOCABULARY_ENRICHMENT_PROMPT_TEMPLATE
from services import MistralService, GroqService, AzureSpeechService

# Initialisation
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
Config.validate()

# Services
mistral = MistralService()
groq = GroqService()
azure_speech = AzureSpeechService()


# ==================== UTILITAIRES ====================

def clean_json(text):
    """Nettoyer le JSON des balises markdown"""
    text = text.strip()
    if text.startswith('```json'):
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
    elif text.startswith('```'):
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
    return text


def clean_whitespace(text):
    """Nettoyer les espaces multiples"""
    return re.sub(r'\s+', ' ', text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')).strip()


# ==================== ROUTES ====================

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
        
        # Initialiser l'historique avec le prompt système à jour
        if 'history' not in session:
            session['history'] = [{"role": "system", "content": get_system_prompt()}]
        
        history = session['history']
        history.append({"role": "user", "content": user_message})
        
        # Appeler Mistral
        response = mistral.chat_complete(history)
        
        # Parser le JSON
        cleaned = clean_json(response)
        try:
            parsed = json.loads(cleaned)
            text = clean_whitespace(parsed.get('text', ''))
            vocabulary = parsed.get('vocabulary', [])
            
            for item in vocabulary:
                if 'translation' in item:
                    item['translation'] = clean_whitespace(item['translation'])
                if 'word' in item:
                    item['word'] = clean_whitespace(item['word'])
        except json.JSONDecodeError as e:
            print(f"JSON error: {e}")
            text = clean_whitespace(response)
            vocabulary = []
        
        # Ajouter à l'historique et limiter
        history.append({"role": "assistant", "content": text})
        if len(history) > Config.MAX_HISTORY_LENGTH:
            history = [history[0]] + history[-50:]
        session['history'] = history
        
        return jsonify({'response': text, 'vocabulary': vocabulary, 'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/reset', methods=['POST'])
def reset():
    """Réinitialiser la conversation"""
    session.clear()
    return jsonify({'success': True})


@app.route('/translate', methods=['POST'])
def translate():
    """Traduire un texte grec en français"""
    try:
        greek_text = request.json.get('text', '').strip()
        if not greek_text:
            return jsonify({'error': 'Texte vide'}), 400
        
        prompt = TRANSLATION_PROMPT_TEMPLATE.format(text=greek_text)
        translation = mistral.simple_query(prompt)
        
        return jsonify({'translation': translation, 'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/enrich-vocabulary', methods=['POST'])
def enrich_vocabulary():
    """Enrichir le vocabulaire avec exemples et conjugaisons"""
    try:
        words = request.json.get('words', [])
        if not words:
            return jsonify({'words': [], 'success': True})
        
        words_list = ', '.join([f'"{w}"' for w in words])
        prompt = VOCABULARY_ENRICHMENT_PROMPT_TEMPLATE.format(words_list=words_list)
        response = mistral.simple_query(prompt)
        
        cleaned = clean_json(response)
        enriched = json.loads(cleaned)
        
        return jsonify({'words': enriched.get('words', []), 'success': True})
        
    except Exception as e:
        print(f"Enrichment error: {e}")
        return jsonify({'words': [], 'success': False, 'error': str(e)}), 500


@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Transcrire l'audio avec Groq Whisper"""
    try:
        if not Config.GROQ_API_KEY:
            return jsonify({'error': 'Groq API key not configured', 'success': False}), 500
        
        audio_data = request.json.get('audio', '')
        prompt_hint = request.json.get('prompt', None)  # Contexte optionnel
        
        if not audio_data:
            return jsonify({'error': 'Pas de données audio'}), 400
        
        # Décoder base64
        if ',' in audio_data:
            audio_data = audio_data.split(',')[1]
        audio_bytes = base64.b64decode(audio_data)
        
        print(f"[Transcribe] Audio reçu: {len(audio_bytes)} bytes", file=sys.stderr)
        
        # Transcrire avec contexte
        text = groq.transcribe(audio_bytes, prompt_hint)
        
        print(f"[Transcribe] Résultat: {text}", file=sys.stderr)
        
        return jsonify({'text': text, 'success': True})
        
    except Exception as e:
        print(f"Transcription error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/speak', methods=['POST'])
def speak():
    """Synthèse vocale avec Azure Speech"""
    print("[SPEAK] Début de la requête", file=sys.stderr)
    
    try:
        if not Config.AZURE_SPEECH_KEY or not Config.AZURE_SPEECH_REGION:
            print("[SPEAK] Erreur: Azure Speech non configuré", file=sys.stderr)
            return jsonify({'error': 'Azure Speech non configuré', 'success': False}), 500
        
        text = request.json.get('text', '').strip()
        if not text:
            print("[SPEAK] Erreur: texte vide", file=sys.stderr)
            return jsonify({'error': 'Texte vide'}), 400
        
        print(f"[SPEAK] Texte reçu: {text[:100]}...", file=sys.stderr)
        
        # Générer l'audio
        print("[SPEAK] Appel à azure_speech.text_to_speech...", file=sys.stderr)
        audio_base64 = azure_speech.text_to_speech(text)
        
        print(f"[SPEAK] Audio généré avec succès: {len(audio_base64)} caractères base64", file=sys.stderr)
        
        return jsonify({
            'audio': audio_base64,
            'success': True
        })
        
    except Exception as e:
        print(f"[SPEAK] ERREUR: {type(e).__name__}: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'success': False}), 500


# ==================== LANCEMENT ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🇬🇷 Σωκράτης 2.0")
    print("=" * 60)
    print("🔊 Voix: Azure Speech (el-GR-NestorasNeural)")
    print("🎤 Reconnaissance: Groq Whisper avec post-correction")
    app.run(debug=True, host='0.0.0.0', port=5000)