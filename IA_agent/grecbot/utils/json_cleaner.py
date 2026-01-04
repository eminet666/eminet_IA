"""
Utilitaires pour nettoyer et parser le JSON des réponses AI
"""
import json
import re


def clean_markdown_json(text):
    """
    Nettoyer le JSON qui pourrait être entouré de balises markdown
    
    Args:
        text (str): Texte potentiellement avec ```json ou ```
    
    Returns:
        str: Texte nettoyé
    """
    cleaned = text.strip()
    
    if cleaned.startswith('```json'):
        cleaned = re.sub(r'^```json\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)
    elif cleaned.startswith('```'):
        cleaned = re.sub(r'^```\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)
    
    return cleaned


def clean_whitespace(text):
    """
    Nettoyer les retours à la ligne et espaces multiples
    
    Args:
        text (str): Texte à nettoyer
    
    Returns:
        str: Texte nettoyé
    """
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def parse_chat_response(raw_response):
    """
    Parser la réponse du chatbot et extraire le texte + vocabulaire
    
    Args:
        raw_response (str): Réponse brute de l'AI
    
    Returns:
        tuple: (text, vocabulary) où text est str et vocabulary est list
    """
    cleaned = clean_markdown_json(raw_response)
    
    try:
        parsed = json.loads(cleaned)
        text = parsed.get('text', '').strip()
        vocabulary = parsed.get('vocabulary', [])
        
        # Nettoyer le texte
        text = clean_whitespace(text)
        
        # Nettoyer le vocabulaire
        for item in vocabulary:
            if 'translation' in item:
                item['translation'] = clean_whitespace(item['translation'])
            if 'word' in item:
                item['word'] = clean_whitespace(item['word'])
        
        return text, vocabulary
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {raw_response}")
        # Fallback : retourner le texte brut nettoyé
        text = clean_whitespace(raw_response)
        return text, []


def parse_vocabulary_response(raw_response):
    """
    Parser la réponse d'enrichissement de vocabulaire
    
    Args:
        raw_response (str): Réponse brute de l'AI
    
    Returns:
        list: Liste des mots enrichis
    """
    cleaned = clean_markdown_json(raw_response)
    
    try:
        parsed = json.loads(cleaned)
        return parsed.get('words', [])
    except json.JSONDecodeError as e:
        print(f"Vocabulary parsing error: {e}")
        return []