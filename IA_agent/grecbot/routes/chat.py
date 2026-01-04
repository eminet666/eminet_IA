"""
Routes pour le chat
"""
from flask import Blueprint, request, jsonify, session
from services.mistral_service import MistralService
from utils.json_cleaner import parse_chat_response
from prompts import SYSTEM_PROMPT
from config import Config

chat_bp = Blueprint('chat', __name__)
mistral_service = MistralService()


@chat_bp.route('/chat', methods=['POST'])
def chat():
    """Endpoint pour les messages de chat"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message vide'}), 400
        
        # Initialiser l'historique si nécessaire
        if 'history' not in session:
            session['history'] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
        
        history = session['history']
        history.append({"role": "user", "content": user_message})
        
        # Appeler Mistral
        assistant_message = mistral_service.chat_complete(history)
        
        # Parser la réponse
        text, vocabulary = parse_chat_response(assistant_message)
        
        # Ajouter à l'historique
        history.append({"role": "assistant", "content": text})
        
        # Limiter l'historique
        if len(history) > Config.MAX_HISTORY_LENGTH:
            history = [history[0]] + history[-50:]
        
        session['history'] = history
        
        return jsonify({
            'response': text,
            'vocabulary': vocabulary,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@chat_bp.route('/reset', methods=['POST'])
def reset():
    """Réinitialiser la conversation"""
    session.clear()
    return jsonify({'success': True, 'message': 'Conversation réinitialisée'})