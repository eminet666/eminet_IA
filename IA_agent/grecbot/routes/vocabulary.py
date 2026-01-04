"""
Routes pour l'enrichissement du vocabulaire
"""
from flask import Blueprint, request, jsonify
from services.mistral_service import MistralService
from utils.json_cleaner import parse_vocabulary_response
from prompts import VOCABULARY_ENRICHMENT_PROMPT_TEMPLATE

vocabulary_bp = Blueprint('vocabulary', __name__)
mistral_service = MistralService()


@vocabulary_bp.route('/enrich-vocabulary', methods=['POST'])
def enrich_vocabulary():
    """Enrichir le vocabulaire avec exemples et formes verbales"""
    try:
        data = request.json
        words = data.get('words', [])
        
        if not words:
            return jsonify({'words': [], 'success': True})
        
        # Créer le prompt
        words_list = ', '.join([f'"{w}"' for w in words])
        prompt = VOCABULARY_ENRICHMENT_PROMPT_TEMPLATE.format(words_list=words_list)
        
        # Appeler Mistral
        raw_response = mistral_service.simple_query(prompt)
        
        # Parser la réponse
        enriched_words = parse_vocabulary_response(raw_response)
        
        return jsonify({
            'words': enriched_words,
            'success': True
        })
        
    except Exception as e:
        print(f"Enrichment error: {e}")
        return jsonify({
            'words': [],
            'success': False,
            'error': str(e)
        }), 500