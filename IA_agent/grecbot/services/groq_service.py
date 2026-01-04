"""
Service pour interagir avec l'API Groq (Whisper)
"""
import requests
import tempfile
import os
from config import Config


class GroqService:
    """Service pour la transcription audio avec Groq Whisper"""
    
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.GROQ_WHISPER_MODEL
        self.api_url = "https://api.groq.com/openai/v1/audio/transcriptions"
    
    def transcribe_audio(self, audio_bytes):
        """
        Transcrire des données audio en texte
        
        Args:
            audio_bytes (bytes): Données audio brutes
        
        Returns:
            str: Texte transcrit
        
        Raises:
            Exception: Si la transcription échoue
        """
        if not self.api_key:
            raise ValueError("GROQ_API_KEY non configuré")
        
        # Sauvegarder temporairement
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            with open(temp_path, 'rb') as audio_file:
                files = {
                    'file': ('audio.webm', audio_file, 'audio/webm'),
                    'model': (None, self.model),
                    'language': (None, 'el')
                }
                
                response = requests.post(self.api_url, headers=headers, files=files)
                result = response.json()
            
            if 'error' in result:
                raise Exception(result.get('error', {}).get('message', 'Erreur inconnue'))
            
            return result.get('text', '').strip()
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)