from flask import Flask, render_template, request, jsonify, session
from mistralai import Mistral
from dotenv import load_dotenv
import os
import secrets

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(16))

# Configuration Mistral
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "mistral-large-latest"

# Prompt système
SYSTEM_PROMPT = """Είσαι ένας φιλικός βοηθός που μιλάει ελληνικά. 
Στόχος σου είναι να κάνεις φυσικές συνομιλίες στα νέα ελληνικά.
Ο συνομιλητής σου έχει επίπεδο C1 στα ελληνικά, οπότε μπορείς να χρησιμοποιείς:
- Σύνθετο λεξιλόγιο και ιδιωματισμούς
- Αποχρώσεις και λεπτές διακρίσεις στη γλώσσα
- Πολιτιστικές αναφορές και σύγχρονες εκφράσεις
- Διάφορα μητρώα γλώσσας (επίσημο, ανεπίσημο)
Απάντα πάντα στα ελληνικά με φυσικό και ευφράδη τρόπο, όπως θα μιλούσες με έναν προχωρημένο μαθητή."""

@app.route('/')
def index():
    """Page d'accueil"""
    session.clear()  # Nouvelle session
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint pour les messages de chat"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message vide'}), 400
        
        # Récupérer ou initialiser l'historique
        if 'history' not in session:
            session['history'] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
        
        history = session['history']
        
        # Ajouter le message utilisateur
        history.append({"role": "user", "content": user_message})
        
        # Appeler Mistral API
        client = Mistral(api_key=MISTRAL_API_KEY)
        response = client.chat.complete(
            model=MODEL,
            messages=history
        )
        
        # Extraire la réponse
        assistant_message = response.choices[0].message.content
        
        # Ajouter à l'historique
        history.append({"role": "assistant", "content": assistant_message})
        
        # Sauvegarder l'historique (limiter à 50 messages pour éviter les sessions trop grandes)
        if len(history) > 52:  # 1 system + 50 messages + 1 nouveau
            history = [history[0]] + history[-50:]
        
        session['history'] = history
        
        return jsonify({
            'response': assistant_message,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/reset', methods=['POST'])
def reset():
    """Réinitialiser la conversation"""
    session.clear()
    return jsonify({'success': True, 'message': 'Conversation réinitialisée'})

if __name__ == '__main__':
    if not MISTRAL_API_KEY:
        print("⚠️  ERREUR: MISTRAL_API_KEY non trouvée dans les variables d'environnement!")
        exit(1)
    
    # Pour le développement local
    app.run(debug=True, host='0.0.0.0', port=5000)