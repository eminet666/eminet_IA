"""
Service pour l'envoi d'emails via SMTP
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import Config
from services.email_templates import get_pdf_email_subject, get_pdf_email_body, get_pdf_filename


class EmailService:
    """Service pour l'envoi d'emails"""
    
    def __init__(self):
        self.smtp_server = Config.EMAIL_SMTP_SERVER
        self.smtp_port = Config.EMAIL_SMTP_PORT
        self.email_address = Config.EMAIL_ADDRESS
        self.email_password = Config.EMAIL_PASSWORD
        self.timeout = Config.EMAIL_TIMEOUT
    
    def validate_config(self):
        """Vérifier que la configuration email est valide"""
        if not self.email_password:
            raise ValueError("EMAIL_PASSWORD non configuré")
    
    def send_pdf_email(self, pdf_bytes, dialogue, recipient=None):
        """
        Envoyer un PDF par email
        
        Args:
            pdf_bytes (bytes): Données du PDF
            dialogue (str): Texte du dialogue pour le corps de l'email
            recipient (str, optional): Destinataire (par défaut: EMAIL_ADDRESS)
        
        Returns:
            dict: {'success': bool, 'message': str}
        
        Raises:
            Exception: Si l'envoi échoue
        """
        self.validate_config()
        
        if recipient is None:
            recipient = self.email_address
        
        # Vérifier la taille du PDF
        pdf_size_mb = len(pdf_bytes) / (1024 * 1024)
        if pdf_size_mb > Config.PDF_MAX_SIZE_MB:
            raise ValueError(f'PDF trop volumineux ({pdf_size_mb:.2f} MB > {Config.PDF_MAX_SIZE_MB} MB)')
        
        print(f"📧 Préparation email pour {recipient}")
        print(f"📄 Taille PDF: {pdf_size_mb:.2f} MB")
        
        # Créer le message
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = recipient
        msg['Subject'] = get_pdf_email_subject()
        
        # Corps de l'email
        body = get_pdf_email_body(dialogue)
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Pièce jointe PDF
        filename = get_pdf_filename()
        attachment = MIMEBase('application', 'pdf')
        attachment.set_payload(pdf_bytes)
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(attachment)
        
        # Envoyer
        print(f"📨 Connexion à {self.smtp_server}:{self.smtp_port}...")
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=self.timeout) as server:
            server.starttls()
            print(f"🔐 Authentification...")
            server.login(self.email_address, self.email_password)
            print(f"✉️ Envoi du message...")
            server.send_message(msg)
        
        print(f"✅ Email envoyé avec succès à {recipient}!")
        
        return {
            'success': True,
            'message': f'Email envoyé à {recipient}'
        }