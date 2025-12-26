from mistralai import Mistral
from dotenv import load_dotenv
import os
import sys

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration
API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "mistral-large-latest"  # Le meilleur modèle pour les conversations multilingues

def create_greek_bot():
    """Crée un bot conversationnel en grec moderne"""
    client = Mistral(api_key=API_KEY)
    
    # Prompt système pour optimiser les conversations en grec
    system_prompt = """Είσαι ένας φιλικός βοηθός που μιλάει ελληνικά. 
Στόχος σου είναι να κάνεις φυσικές συνομιλίες στα νέα ελληνικά.
Απάντα πάντα στα ελληνικά, χρησιμοποιώντας σύγχρονη και φυσική γλώσσα.
Είσαι υπομονετικός και βοηθάς τον συνομιλητή σου να βελτιώσει τα ελληνικά του."""
    
    # Historique de conversation
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    print("=" * 60)
    print("Bot Συνομιλίας στα Ελληνικά - Mistral AI")
    print("=" * 60)
    print("Γράψε 'έξοδος' ή 'exit' για να τερματίσεις")
    print("=" * 60)
    print()
    
    while True:
        # Demander l'entrée utilisateur
        user_input = input("Εσύ: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['έξοδος', 'exit', 'quit', 'τέλος']:
            print("\nΑντίο! Καλή συνέχεια! 👋")
            break
        
        # Ajouter le message utilisateur
        messages.append({"role": "user", "content": user_input})
        
        try:
            # Appeler l'API Mistral
            response = client.chat.complete(
                model=MODEL,
                messages=messages
            )
            
            # Extraire la réponse
            assistant_message = response.choices[0].message.content
            
            # Ajouter à l'historique
            messages.append({"role": "assistant", "content": assistant_message})
            
            # Afficher la réponse
            print(f"\nBot: {assistant_message}\n")
            
        except Exception as e:
            print(f"\n❌ Σφάλμα: {str(e)}\n")
            # Retirer le dernier message en cas d'erreur
            messages.pop()

if __name__ == "__main__":
    # Vérifier que la clé API est configurée
    if not API_KEY:
        print("⚠️  ATTENTION: Clé API Mistral non trouvée!")
        print("1. Créez un fichier '.env' dans le même dossier que ce script")
        print("2. Ajoutez la ligne: MISTRAL_API_KEY=votre_clé_api")
        sys.exit(1)
    
    create_greek_bot()