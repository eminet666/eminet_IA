"""
Templates d'emails pour l'application Σωκράτης 2.0
"""
from datetime import datetime


def get_pdf_email_subject():
    """Générer le sujet de l'email"""
    return f'Conversation Σωκράτης 2.0 - {datetime.now().strftime("%Y-%m-%d")}'


def get_pdf_email_body(dialogue):
    """
    Générer le corps de l'email avec le dialogue
    
    Args:
        dialogue (str): Le dialogue de la session
    
    Returns:
        str: Le corps de l'email formaté
    """
    return f"""Bonjour,

Voici votre conversation avec Σωκράτης 2.0.

DIALOGUE DE LA SESSION

{dialogue}

Le PDF en pièce jointe contient la conversation complète avec le vocabulaire enrichi (exemples d'usage et conjugaisons).

Καλή συνέχεια!

---
Σωκράτης 2.0 Bot
"""


def get_pdf_filename():
    """Générer le nom du fichier PDF"""
    return f'Socrate_{datetime.now().strftime("%Y-%m-%d")}.pdf'