import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mistralai import Mistral
from datetime import datetime

# Charger le fichier .env
load_dotenv()

# Charger les variables d'environnement
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

# Vérification des clés
if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY n'est pas définie dans les variables d'environnement")
if not GMAIL_USER or not GMAIL_PASSWORD:
    raise ValueError("GMAIL_USER ou GMAIL_PASSWORD manquant")

print(f"- API Key chargée ...")

# Initialiser le client Mistral
client = Mistral(api_key=MISTRAL_API_KEY)

def generate_greek_dialogue():
    prompt = """
    Crée un dialogue en grec moderne (niveau B2) entre Stephanos et Anna, sur le sujet suivant : {sujet}
    
    Le dialogue doit faire environ une page A4 (environ 500 mots).
    
    FORMATAGE DU DIALOGUE :
    - Commence par un titre en grec en rapport avec le sujet du dialogue, au format : <h3>Titre en grec</h3>
    - Exemple : <h3>Στο Σουπερμάρκετ</h3> ou <h3>Μια Συζήτηση για τον Καιρό</h3>
    - Ensuite, chaque réplique doit être dans une balise <p> séparée
    - Format : <p><strong>Nom du personnage :</strong> texte de la réplique</p>
    - Exemple : <p><strong>Στέφανος:</strong> Γεια σου Άννα! Τι κάνεις;</p>
    - Chaque réplique dans son propre paragraphe <p> pour créer un retour à la ligne automatique
    
    VOCABULAIRE :
    Après le dialogue, ajoute une section "Λεξιλόγιο" (Vocabulaire) avec un tableau HTML.
    
    Le tableau doit avoir 3 colonnes :
    - Colonne 1 : Mot en grec (en gras)
    - Colonne 2 : Traduction en français
    - Colonne 3 : Phrase d'exemple en grec
    
    Utilise ce format de tableau :
    <table class="vocab-table">
        <thead>
            <tr>
                <th>Grec</th>
                <th>Français</th>
                <th>Exemple</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>mot grec</strong></td>
                <td>traduction</td>
                <td>phrase d'exemple</td>
            </tr>
        </tbody>
    </table>
    
    Assure-toi que le vocabulaire contient environ 20-25 mots clés du dialogue.
    """
    
    # Liste de sujets
    sujets = [
        "Les courses au marché", "Un dîner en famille",
        "Une sortie au cinéma", "Un problème de voisinage",
        "Un voyage en bus", "Une discussion sur la météo"
    ]
    
    sujet = sujets[datetime.now().day % len(sujets)]
    
    # Utilisation de la méthode chat.complete
    chat_response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt.format(sujet=sujet)}]
    )
    
    return chat_response.choices[0].message.content

def send_email(content):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = "eminet666@gmail.com"
    msg["Subject"] = "Ton dialogue grec quotidien"
    
    # Utilisation de HTML pour un meilleur affichage dans l'email
    html_content = f"""
    <html>
        <head>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    line-height: 1.8; 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 20px;
                }}
                h2 {{ 
                    color: #2c3e50; 
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h3 {{
                    color: #34495e;
                    margin-top: 30px;
                }}
                .dialogue {{ 
                    background-color: #f9f9f9; 
                    padding: 20px; 
                    border-radius: 8px;
                    border-left: 4px solid #3498db;
                }}
                .dialogue p {{
                    margin: 10px 0;
                }}
                .vocab-table {{ 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin-top: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .vocab-table th {{ 
                    background-color: #3498db; 
                    color: white;
                    padding: 12px 8px;
                    text-align: left;
                    font-weight: bold;
                }}
                .vocab-table td {{ 
                    border: 1px solid #ddd; 
                    padding: 10px 8px; 
                    text-align: left; 
                }}
                .vocab-table tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                .vocab-table tr:hover {{
                    background-color: #e8f4f8;
                }}
            </style>
        </head>
        <body>
            <h2>📚 Dialogue en grec moderne</h2>
            <div class="dialogue">
                {content}
            </div>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    dialogue = generate_greek_dialogue()
    print(f"- dialogue généré ...")
    # print(dialogue)
    send_email(dialogue)
    print(f"- dialogue envoyé par email.")