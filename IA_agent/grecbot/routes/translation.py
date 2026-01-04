"""
Routes pour la traduction
"""
from flask import Blueprint, request, jsonify
from services.mistral_service import MistralService
from prompts import TRANSLATION_PROMPT_TEMPLATE

translation_bp = Blueprint('translation', __name__)
mistral_service = MistralService()


@translation_bp.route('/translate', methods=['POST'])
def translate():
    """Traduire un texte grec en français"""
    try:
        data = request.json
        greek_text = data.get('text', '').strip()
        
        if not greek_text:
            return jsonify({'error': 'Texte vide'}), 400
        
        # Créer le prompt de traduction
        prompt = TRANSLATION_PROMPT_TEMPLATE.format(text=greek_text)
        
        # Appeler Mistral
        translation = mistral_service.simple_query(prompt)
        
        return jsonify({
            'translation': translation,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500