"""
Routes pour la transcription audio
"""
from flask import Blueprint, request, jsonify
import base64
from services.groq_service import GroqService
from config import Config

transcription_bp = Blueprint('transcription', __name__)
groq_service = GroqService()


@transcription_bp.route('/transcribe', methods=['POST'])
def transcribe():
    """Transcrire l'audio en texte avec Whisper sur Groq"""
    try:
        if not Config.GROQ_API_KEY:
            return jsonify({
                'error': 'Groq API key not configured',
                'success': False
            }), 500
        
        data = request.json
        audio_data = data.get('audio', '')
        
        if not audio_data:
            return jsonify({'error': 'Pas de données audio'}), 400
        
        # Décoder le base64
        if ',' in audio_data:
            audio_data = audio_data.split(',')[1]
        
        audio_bytes = base64.b64decode(audio_data)
        
        # Transcrire
        text = groq_service.transcribe_audio(audio_bytes)
        
        return jsonify({
            'text': text,
            'success': True
        })
        
    except Exception as e:
        print(f"Transcription error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'success': False
        }), 500