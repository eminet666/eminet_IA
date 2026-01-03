import sys
import os
import subprocess

def run(cmd):
    """Exécute une commande et stoppe si erreur"""
    print("Exécution :", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    if len(sys.argv) != 3:
        print("Usage: python process_video.py fichier.mp4 piste_audio")
        print("Exemple: python process_video.py video.mp4 3")
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
    run(["MP4Box", "-add", f"{input_file}#video", "-add", f"{input_file}#audio{audio_number}", output_audio])

    # 2️⃣ Ré-indexer le MP4 pour compatibilité FFmpeg
    fixed_output = f"{base}_fixed{ext}"
    run(["MP4Box", "-inter", "500", output_audio, "-out", fixed_output])

    # 3️⃣ Appeler le script de traduction sur le MP4 fixé
    run(["python", "traduire_video.py", fixed_output])

    print("\n✅ Traitement terminé. Fichier prêt :", fixed_output)

if __name__ == "__main__":
    main()
