"""
Application Flask - Σωκράτης 2.0
Chatbot pour l'apprentissage du grec moderne (niveau C1)
"""
from flask import Flask, render_template, session
from config import Config
from routes import register_routes

# Initialisation de l'application
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Validation de la configuration
Config.validate()

# Enregistrement des routes
register_routes(app)


# ==================== ROUTE PRINCIPALE ====================

@app.route('/')
def index():
    """Page d'accueil"""
    session.clear()
    return render_template('index.html')


# ==================== LANCEMENT ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🇬🇷 Σωκράτης 2.0 - Chatbot d'apprentissage du grec")
    print("=" * 60)
    print(f"📡 Modèle Mistral: {Config.MISTRAL_MODEL}")
    print(f"📧 Email configuré: {Config.EMAIL_ADDRESS}")
    print(f"🎤 Transcription Groq: {'✅' if Config.GROQ_API_KEY else '❌'}")
    print("=" * 60)
    print("🚀 Serveur démarré sur http://127.0.0.1:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)