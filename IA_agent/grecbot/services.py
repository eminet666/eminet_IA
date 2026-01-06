"""
Services pour l'application Σωκράτης 2.0
Regroupe les services Mistral, Groq, Email et Edge TTS
"""
from mistralai import Mistral
import requests
import tempfile
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from config import Config
import base64
import asyncio
import edge_tts


# ==================== MISTRAL SERVICE ====================

class MistralService:
    """Service pour interagir avec l'API Mistral AI"""
    
    def __init__(self):
        self.client = Mistral(api_key=Config.MISTRAL_API_KEY)
        self.model = Config.MISTRAL_MODEL
    
    def chat_complete(self, messages):
        """
        Compléter une conversation
        
        Args:
            messages (list): Liste des messages de l'historique
        
        Returns:
            str: Réponse de l'assistant
        """
        response = self.client.chat.complete(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
    
    def simple_query(self, prompt):
        """
        Requête simple (sans historique)
        
        Args:
            prompt (str): Le prompt à envoyer
        
        Returns:
            str: Réponse de l'assistant
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat_complete(messages)


# ==================== GROQ SERVICE ====================

class GroqService:
    """Service pour la transcription audio avec Groq Whisper"""
    
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.GROQ_WHISPER_MODEL
        self.api_url = "https://api.groq.com/openai/v1/audio/transcriptions"
    
    def transcribe(self, audio_bytes):
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
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
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


# ==================== EDGE TTS SERVICE (GRATUIT) ====================

class EdgeTTSService:
    """Service pour la synthèse vocale avec Edge TTS (Microsoft, gratuit illimité)"""
    
    def __init__(self):
        # Voix grecque masculine disponibles :
        # el-GR-NestorasNeural (homme, neutre, recommandé pour Socrate)
        self.voice = "el-GR-NestorasNeural"
        self.rate = "-15%"  # Légèrement plus lent (Socrate réfléchi)
        self.pitch = "-5Hz"  # Voix plus grave
    
    async def _generate_audio(self, text):
        """Générer l'audio de manière asynchrone"""
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            pitch=self.pitch
        )
        
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return audio_data
    
    def text_to_speech(self, text):
        """
        Convertir du texte en audio avec voix masculine grecque
        
        Args:
            text (str): Texte à synthétiser
        
        Returns:
            str: Audio encodé en base64 (format MP3)
        
        Raises:
            Exception: Si la synthèse échoue
        """
        try:
            # Nettoyer le texte des emojis
            clean_text = text.replace('🔊', '').replace('🇫🇷', '').replace('🎤', '').replace('➤', '').strip()
            
            # Exécuter la fonction async
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            audio_bytes = loop.run_until_complete(self._generate_audio(clean_text))
            loop.close()
            
            # Encoder en base64
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            return audio_base64
            
        except Exception as e:
            raise Exception(f"Erreur Edge TTS: {str(e)}")


# ==================== EMAIL SERVICE ====================

class EmailService:
    """Service pour l'envoi d'emails via SMTP"""
    
    def __init__(self):
        self.smtp_server = Config.EMAIL_SMTP_SERVER
        self.smtp_port = Config.EMAIL_SMTP_PORT
        self.email_address = Config.EMAIL_ADDRESS
        self.email_password = Config.EMAIL_PASSWORD
        self.timeout = Config.EMAIL_TIMEOUT
    
    def send_pdf(self, pdf_bytes, dialogue, recipient=None):
        """
        Envoyer un PDF par email
        
        Args:
            pdf_bytes (bytes): Données du PDF
            dialogue (str): Texte du dialogue pour le corps de l'email
            recipient (str, optional): Destinataire
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        print("=== DEBUT EmailService.send_pdf ===")
        
        if not self.email_password:
            print("❌ EMAIL_PASSWORD non configuré")
            raise ValueError("EMAIL_PASSWORD non configuré")
        
        if recipient is None:
            recipient = self.email_address
        
        # Vérifier la taille
        pdf_size_mb = len(pdf_bytes) / (1024 * 1024)
        print(f"📄 Taille PDF: {pdf_size_mb:.2f} MB")
        
        if pdf_size_mb > Config.PDF_MAX_SIZE_MB:
            raise ValueError(f'PDF trop volumineux ({pdf_size_mb:.2f} MB > {Config.PDF_MAX_SIZE_MB} MB)')
        
        print(f"📧 Destinataire: {recipient}")
        
        # Créer le message
        print("📝 Création du message email...")
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = recipient
        msg['Subject'] = f'Conversation Σωκράτης 2.0 - {datetime.now().strftime("%Y-%m-%d")}'
        
        # Corps de l'email
        body = f"""Bonjour,

Voici votre conversation avec Σωκράτης 2.0.

DIALOGUE DE LA SESSION

{dialogue}

Le PDF en pièce jointe contient la conversation complète avec le vocabulaire enrichi (exemples d'usage et conjugaisons).

Καλή συνέχεια!

---
Σωκράτης 2.0 Bot
"""
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Pièce jointe PDF
        print("📎 Ajout de la pièce jointe PDF...")
        filename = f'Socrate_{datetime.now().strftime("%Y-%m-%d")}.pdf'
        attachment = MIMEBase('application', 'pdf')
        attachment.set_payload(pdf_bytes)
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(attachment)
        
        # Envoyer
        print(f"📨 Connexion SMTP à {self.smtp_server}:{self.smtp_port}...")
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=self.timeout) as server:
                print("🔐 STARTTLS...")
                server.starttls()
                print("🔑 Authentification...")
                server.login(self.email_address, self.email_password)
                print("📤 Envoi du message...")
                server.send_message(msg)
            
            print(f"✅ Email envoyé avec succès à {recipient}!")
            
            return {
                'success': True,
                'message': f'Email envoyé à {recipient}'
            }
        except smtplib.SMTPException as e:
            print(f"❌ Erreur SMTP: {type(e).__name__}: {str(e)}")
            raise