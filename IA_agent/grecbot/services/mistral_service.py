"""
Service pour interagir avec l'API Mistral AI
"""
from mistralai import Mistral
from config import Config


class MistralService:
    """Service pour gérer les appels à Mistral AI"""
    
    def __init__(self):
        self.client = Mistral(api_key=Config.MISTRAL_API_KEY)
        self.model = Config.MISTRAL_MODEL
    
    def chat_complete(self, messages):
        """
        Compléter une conversation
        
        Args:
            messages (list): Liste des messages de l'historique
        
        Returns:
            str: Réponse de l'assistant
        """
        response = self.client.chat.complete(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
    
    def simple_query(self, prompt):
        """
        Requête simple (sans historique)
        
        Args:
            prompt (str): Le prompt à envoyer
        
        Returns:
            str: Réponse de l'assistant
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat_complete(messages)