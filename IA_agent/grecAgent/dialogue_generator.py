# dialogue_generator.py
# Génération du dialogue avec Mistral AI

from mistralai import Mistral
from datetime import datetime
import re
from config import DIALOGUE_TOPICS, DIALOGUE_PROMPT


def generate_greek_dialogue(client):
    """
    Génère un dialogue en grec avec Mistral AI
    """
    # Sélectionner un sujet en fonction du jour
    sujet = DIALOGUE_TOPICS[datetime.now().day % len(DIALOGUE_TOPICS)]
    
    # Appel à l'API Mistral
    chat_response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": DIALOGUE_PROMPT.format(sujet=sujet)}]
    )
    
    return chat_response.choices[0].message.content


def extract_title(html_content):
    """
    Extrait le titre du dialogue depuis la balise <h3>
    """
    title_pattern = r'<h3>(.*?)</h3>'
    match = re.search(title_pattern, html_content, re.IGNORECASE | re.DOTALL)
    
    if match:
        title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        return title
    
    return None


def extract_dialogue_lines(html_content):
    """
    Extrait les répliques du dialogue HTML et retourne une liste de tuples (speaker, text)
    """
    dialogue_lines = []
    
    # Pattern pour extraire les répliques : <p><strong>Nom:</strong> texte</p>
    pattern = r'<p><strong>(Στέφανος|Άννα):</strong>\s*(.*?)</p>'
    matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
    
    for speaker, text in matches:
        # Nettoyer le texte des balises HTML résiduelles
        clean_text = re.sub(r'<[^>]+>', '', text).strip()
        
        # Normaliser les noms pour la comparaison
        speaker_normalized = "Stephanos" if "Στέφανος" in speaker else "Anna"
        
        dialogue_lines.append((speaker_normalized, clean_text))
    
    return dialogue_lines