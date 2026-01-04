"""
Routes pour l'envoi d'emails
"""
from flask import Blueprint, request, jsonify
import base64
import smtplib
from services.email_service import EmailService
from config import Config

email_bp = Blueprint('email', __name__)
email_service = EmailService()


@email_bp.route('/send-pdf-email', methods=['POST'])
def send_pdf_email():
    """Envoyer le PDF par email"""
    try:
        # Vérifier la configuration
        if not Config.EMAIL_PASSWORD:
            print("⚠️ EMAIL_PASSWORD non configuré")
            return jsonify({
                'error': 'Configuration email manquante.',
                'success': False
            }), 400
        
        data = request.json
        pdf_data = data.get('pdf', '')
        dialogue = data.get('dialogue', '')
        recipient = data.get('email', Config.EMAIL_ADDRESS)
        
        if not pdf_data:
            return jsonify({'error': 'Pas de données PDF'}), 400
        
        # Décoder le base64
        if ',' in pdf_data:
            pdf_data = pdf_data.split(',')[1]
        
        pdf_bytes = base64.b64decode(pdf_data)
        
        # Envoyer l'email
        result = email_service.send_pdf_email(pdf_bytes, dialogue, recipient)
        
        return jsonify(result)
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = "Erreur d'authentification Gmail. Vérifiez le mot de passe d'application."
        print(f"❌ {error_msg}: {e}")
        return jsonify({
            'error': error_msg,
            'success': False
        }), 401
    
    except smtplib.SMTPException as e:
        error_msg = f"Erreur SMTP: {str(e)}"
        print(f"❌ {error_msg}")
        return jsonify({
            'error': error_msg,
            'success': False
        }), 500
    
    except ValueError as e:
        print(f"❌ Erreur validation: {e}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 400
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erreur email: {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': error_msg,
            'success': False
        }), 500