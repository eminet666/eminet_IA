# email_sender.py
# Envoi des emails avec les pièces jointes

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from config import EMAIL_RECIPIENTS, ACCENT_COLOR


def send_email(gmail_user, gmail_password, content, audio_file=None, pdf_file=None, title=None):
    """
    Envoie un email avec le dialogue et les pièces jointes
    """
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = ", ".join(EMAIL_RECIPIENTS)
    
    # Créer le subject avec le titre si disponible
    if title:
        msg["Subject"] = f"ritalAgent : {title} - Dialogue italien quotidien"
    else:
        msg["Subject"] = "ritalAgent : Dialogue italien quotidien 🎧"
    
    # Titre pour l'en-tête de l'email
    email_title = f"{title}" if title else "Dialogue en italien (niveau B2)"
    
    # Message d'information sur les pièces jointes
    attachments_info = []
    if audio_file:
        attachments_info.append("🎧 Fichier audio pour améliorer ta prononciation")
    if pdf_file:
        attachments_info.append("📄 PDF à imprimer ou à conserver")
    
    attachments_html = ""
    if attachments_info:
        attachments_html = f"""
        <div class="audio-notice">
            <strong>Pièces jointes incluses :</strong><br>
            {'<br>'.join(attachments_info)}
        </div>
        """
    
    # Utilisation de HTML pour un meilleur affichage dans l'email
    html_content = f"""
    <html>
        <head>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    line-height: 1.5; 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 15px;
                    font-size: 14px;
                }}
                h2 {{ 
                    color: #2c3e50; 
                    border-bottom: 2px solid {ACCENT_COLOR};
                    padding-bottom: 8px;
                    margin-bottom: 12px;
                    font-size: 20px;
                }}
                h3 {{
                    color: #34495e;
                    margin-top: 15px;
                    margin-bottom: 10px;
                    font-size: 16px;
                }}
                .audio-notice {{
                    background-color: #e8f4f8;
                    padding: 10px;
                    border-radius: 4px;
                    margin: 12px 0;
                    font-size: 12px;
                }}
                .dialogue {{ 
                    background-color: #f9f9f9; 
                    padding: 12px; 
                    border-radius: 5px;
                }}
                .dialogue p {{
                    margin: 6px 0;
                }}
                .vocab-table {{ 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin-top: 12px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    font-size: 14px;
                }}
                .vocab-table th {{ 
                    background-color: {ACCENT_COLOR}; 
                    color: white;
                    padding: 5px 4px;
                    text-align: left;
                    font-weight: bold;
                    font-size: 14px;
                }}
                .vocab-table td {{ 
                    border: 1px solid #ddd; 
                    padding: 4px 5px; 
                    text-align: left; 
                    vertical-align: top;
                    line-height: 1.3;
                }}
                .vocab-table tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                .vocab-table tr:hover {{
                    background-color: #e8f4f8;
                }}
                .vocab-table td:first-child {{
                    width: 18%;
                }}
                .vocab-table td:nth-child(2) {{
                    width: 22%;
                }}
                .vocab-table td:nth-child(3) {{
                    width: 60%;
                }}
            </style>
        </head>
        <body>
            <h2>{email_title}</h2>
            {attachments_html}
            <div class="dialogue">
                {content}
            </div>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    
    # Ajouter le fichier audio en pièce jointe si disponible
    if audio_file and os.path.exists(audio_file):
        try:
            with open(audio_file, "rb") as attachment:
                part = MIMEBase("audio", "mpeg")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            filename = f"dialogue_italien_{datetime.now().strftime('%Y%m%d')}.mp3"
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            
            msg.attach(part)
            print(f"✓ Fichier audio attaché : {filename}")
        except Exception as e:
            print(f"⚠️  Erreur lors de l'attachement du fichier audio : {e}")
    
    # Ajouter le fichier PDF en pièce jointe si disponible
    if pdf_file and os.path.exists(pdf_file):
        try:
            with open(pdf_file, "rb") as attachment:
                part = MIMEBase("application", "pdf")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            filename = f"dialogue_italien_{datetime.now().strftime('%Y%m%d')}.pdf"
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            
            msg.attach(part)
            print(f"✓ Fichier PDF attaché : {filename}")
        except Exception as e:
            print(f"⚠️  Erreur lors de l'attachement du fichier PDF : {e}")
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
