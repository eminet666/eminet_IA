import whisper
import sys
import warnings

# Supprimer les warnings liés à l'utilisation du CPU et FP16
warnings.filterwarnings("ignore", category=UserWarning)

def main():
    if len(sys.argv) != 2:
        print("Usage: python traduire_video.py fichier.mp4")
        sys.exit(1)

    video_file = sys.argv[1]

    # Forcer l'exécution sur CPU
    device = "cpu"
    print(f"Device utilisé pour Whisper : {device}")

    # Chargement du modèle medium
    model = whisper.load_model("medium", device=device)

    # Début de la transcription
    print("Début de la transcription...")
    result = model.transcribe(video_file)

    # Sauvegarde du texte dans un fichier .txt
    output_txt = video_file.replace(".mp4", "_transcription.txt")
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"✅ Transcription terminée. Fichier : {output_txt}")

if __name__ == "__main__":
    main()
