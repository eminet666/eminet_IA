"""
Configuration de l'application Σωκράτης 2.0
"""
import os
import secrets
from dotenv import load_dotenv


# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration principale"""
    
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(16))
    
    # Mistral AI
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    MISTRAL_MODEL = "mistral-large-latest"
    
    # Groq (pour transcription)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_WHISPER_MODEL = "whisper-large-v3"
    
    # Azure Speech (pour synthèse vocale)
    AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
    AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")  # Ex: "westeurope", "eastus"
    
    # Email (Gmail)
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "eminet666@gmail.com")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_SMTP_SERVER = "smtp.gmail.com"
    EMAIL_SMTP_PORT = 587
    EMAIL_TIMEOUT = 60
    
    # Limites
    MAX_HISTORY_LENGTH = 52  # Messages max en session (2 + 50)
    PDF_MAX_SIZE_MB = 25  # Limite Gmail
    
    @classmethod
    def validate(cls):
        """Valider la configuration"""
        if not cls.MISTRAL_API_KEY:
            raise ValueError("⚠️  ERREUR: MISTRAL_API_KEY non trouvée!")
        
        if not cls.EMAIL_PASSWORD:
            print("⚠️  AVERTISSEMENT: EMAIL_PASSWORD non configuré - l'envoi d'emails ne fonctionnera pas")
        
        if not cls.GROQ_API_KEY:
            print("⚠️  AVERTISSEMENT: GROQ_API_KEY non configuré - la transcription vocale iOS ne fonctionnera pas")
        
        if not cls.AZURE_SPEECH_KEY or not cls.AZURE_SPEECH_REGION:
            print("⚠️  AVERTISSEMENT: Azure Speech non configuré - la synthèse vocale ne fonctionnera pas")