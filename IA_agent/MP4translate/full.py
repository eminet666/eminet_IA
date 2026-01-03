import sys
import os
import subprocess

def run(cmd):
    """Exécute une commande et stoppe si erreur"""
    print("\nExécution :", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    if len(sys.argv) != 3:
        print("Usage: python full.py fichier.mp4 piste_audio")
        print("Exemple: python full.py video.mp4 3")
        sys.exit(1)

    input_file = sys.argv[1]
    audio_number = sys.argv[2]

    if not os.path.isfile(input_file):
        print("Fichier introuvable :", input_file)
        sys.exit(1)

    if not audio_number.isdigit() or int(audio_number) < 1:
        print("Numéro de piste audio invalide :", audio_number)
        sys.exit(1)

    base, ext = os.path.splitext(input_file)

    # 1️⃣ Extraire la vidéo et la piste audio choisie
    output_audio = f"{base}_audio{audio_number}{ext}"
    run([
        "MP4Box",
        "-add", f"{input_file}#video",
        "-add", f"{input_file}#audio{audio_number}",
        output_audio
    ])

    # 2️⃣ Ré-indexer le MP4 pour compatibilité FFmpeg / Whisper
    fixed_output = f"{base}_fixed{ext}"
    run(["MP4Box", "-inter", "500", output_audio, "-out", fixed_output])

    # 3️⃣ Appeler le script de traduction (CPU)
    run([sys.executable, "traduire_video.py", fixed_output])

    # 4️⃣ Supprimer les fichiers intermédiaires
    for f in [output_audio, fixed_output]:
        try:
            if os.path.exists(f):
                os.remove(f)
                print(f"Supprimé fichier intermédiaire : {f}")
        except Exception as e:
            print(f"Erreur suppression {f} :", e)

    # 5️⃣ Afficher le fichier final de transcription
    transcription_file = fixed_output.replace(".mp4", "_transcription.txt")
    if os.path.exists(transcription_file):
        print("\n✅ Transcription prête :", transcription_file)
    else:
        print("\n⚠️ Transcription non trouvée !")

if __name__ == "__main__":
    main()
