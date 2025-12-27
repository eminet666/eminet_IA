import os
from groq import Groq
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupère la clé API depuis la variable d'environnement
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("La clé API GROQ_API_KEY n'est pas définie dans le fichier .env")

client = Groq(api_key=api_key)

def transcrire_audio(fichier_audio):
    try:
        with open(fichier_audio, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(fichier_audio, file.read()),
                model="whisper-large-v3",
                response_format="verbose_json"
            )
        return transcription.text
    except AttributeError:
        return "Erreur : La fonctionnalité audio n'est pas disponible avec cette clé API ou cette version de la bibliothèque."
    except Exception as e:
        return f"Erreur lors de la transcription : {e}"

fichier_audio = "test_mp3.mp3"
texte_transcrit = transcrire_audio(fichier_audio)
print("Transcription :", texte_transcrit)
