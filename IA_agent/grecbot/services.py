"""
Services pour l'application Σωκράτης 2.0
Regroupe les services Mistral, Groq, Email et Azure Speech
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
import sys
import re


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
        
        # Dictionnaire de corrections phonétiques courantes
        self.phonetic_corrections = {
            # Erreurs de transcription courantes
            r'\bσα\b': 'θα',           # σα → θα (futur)
            r'\bτα\b': 'θα',           # τα → θα (futur)
            r'\bδεν\s+σα\b': 'δεν θα', # δεν σα → δεν θα
            r'\bσε\s+σα\b': 'θα σε',   # σε σα → θα σε
            
            # Autres confusions phonétiques
            r'\bδα\b': 'θα',           # δα → θα
            r'\bσαν\b': 'θαν',         # σαν → θαν (comme si)
            
            # Corrections de particules
            r'\bνα\s+σα\b': 'να θα',   # να σα → να θα
            r'\bαν\s+σα\b': 'αν θα',   # αν σα → αν θα
            
            # Mots composés mal séparés
            r'\bτι\s+σα\b': 'τι θα',   # τι σα → τι θα
            r'\bπως\s+σα\b': 'πως θα', # πως σα → πως θα
        }
    
    def _post_correct_transcription(self, text):
        """
        Corriger les erreurs phonétiques courantes dans la transcription
        
        Args:
            text (str): Texte transcrit
        
        Returns:
            str: Texte corrigé
        """
        corrected = text
        
        # Appliquer toutes les corrections
        for pattern, replacement in self.phonetic_corrections.items():
            corrected = re.sub(pattern, replacement, corrected, flags=re.IGNORECASE)
        
        return corrected
    
    def transcribe(self, audio_bytes, prompt_hint=None):
        """
        Transcrire des données audio en texte
        
        Args:
            audio_bytes (bytes): Données audio brutes
            prompt_hint (str, optional): Contexte pour améliorer la reconnaissance
        
        Returns:
            str: Texte transcrit et corrigé
        
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
            
            # Prompt enrichi avec vocabulaire C1 et mots courants
            if not prompt_hint:
                prompt_hint = (
                    "Σωκράτης, φιλοσοφία, σοφία, αρετή, γνώση, διάλογος, "
                    "θα, θαν, δεν θα, να θα, αν θα, πώς θα, τι θα"
                )
            
            with open(temp_path, 'rb') as audio_file:
                files = {
                    'file': ('audio.webm', audio_file, 'audio/webm'),
                    'model': (None, self.model),
                    'language': (None, 'el'),
                    'temperature': (None, '0.0'),  # Maximum de précision
                    'prompt': (None, prompt_hint)
                }
                
                response = requests.post(self.api_url, headers=headers, files=files)
                result = response.json()
            
            if 'error' in result:
                raise Exception(result.get('error', {}).get('message', 'Erreur inconnue'))
            
            transcribed_text = result.get('text', '').strip()
            print(f"[Groq] Transcription brute: {transcribed_text}", file=sys.stderr)
            
            # Post-correction
            corrected_text = self._post_correct_transcription(transcribed_text)
            
            if corrected_text != transcribed_text:
                print(f"[Groq] Après correction: {corrected_text}", file=sys.stderr)
            
            return corrected_text
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


# ==================== AZURE SPEECH SERVICE ====================

class AzureSpeechService:
    """Service pour la synthèse vocale avec Azure Speech (Microsoft)"""
    
    def __init__(self):
        self.api_key = Config.AZURE_SPEECH_KEY
        self.region = Config.AZURE_SPEECH_REGION
        
        # URL de l'API (adapté selon la région)
        self.api_url = f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
        
        # Configuration de la voix
        self.voice_name = "el-GR-NestorasNeural"  # Voix masculine grecque
        self.speaking_rate = "-15%"  # Plus lent (Socrate réfléchi)
        self.pitch = "-5Hz"  # Plus grave
    
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
        if not self.api_key or not self.region:
            raise ValueError("AZURE_SPEECH_KEY ou AZURE_SPEECH_REGION non configuré")
        
        # Nettoyer le texte des emojis
        clean_text = text.replace('🔊', '').replace('🇫🇷', '').replace('🎤', '').replace('➤', '').strip()
        
        print(f"[AzureTTS] Génération audio pour: {clean_text[:50]}...", file=sys.stderr)
        
        # Construire le SSML (Speech Synthesis Markup Language)
        ssml = f"""<speak version='1.0' xml:lang='el-GR'>
            <voice name='{self.voice_name}'>
                <prosody rate='{self.speaking_rate}' pitch='{self.pitch}'>
                    {clean_text}
                </prosody>
            </voice>
        </speak>"""
        
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
            "User-Agent": "SocratesBot"
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                data=ssml.encode('utf-8'),
                timeout=30
            )
            
            response.raise_for_status()
            
            # Encoder l'audio en base64
            audio_base64 = base64.b64encode(response.content).decode('utf-8')
            
            print(f"[AzureTTS] Audio généré avec succès: {len(audio_base64)} caractères base64", file=sys.stderr)
            
            return audio_base64
            
        except requests.exceptions.RequestException as e:
            print(f"[AzureTTS] ERREUR: {str(e)}", file=sys.stderr)
            if hasattr(e.response, 'text'):
                print(f"[AzureTTS] Détails: {e.response.text}", file=sys.stderr)
            raise Exception(f"Erreur Azure Speech: {str(e)}")


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