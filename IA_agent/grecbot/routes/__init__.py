"""
Package routes - Enregistrement de toutes les routes
"""
from flask import Blueprint


def register_routes(app):
    """
    Enregistrer toutes les routes dans l'application Flask
    
    Args:
        app: Instance Flask
    """
    from routes.chat import chat_bp
    from routes.translation import translation_bp
    from routes.vocabulary import vocabulary_bp
    from routes.email_service import email_bp
    from routes.transcription import transcription_bp
    
    # Enregistrer les blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(translation_bp)
    app.register_blueprint(vocabulary_bp)
    app.register_blueprint(email_bp)
    app.register_blueprint(transcription_bp)
    
    print("✅ Toutes les routes ont été enregistrées")