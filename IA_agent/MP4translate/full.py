import sys
import os
import subprocess

def run(cmd):
    """Exécute une commande et stoppe si erreur"""
    print("Exécution :", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    if len(sys.argv) != 2:
        print("Usage: python process_video.py fichier.mp4")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print("Fichier introuvable :", input_file)
        sys.exit(1)

    base, ext = os.path.splitext(input_file)

    # 1️⃣ Extraire la vidéo et la piste audio 3
    output_audio3 = f"{base}_audio3{ext}"
    run(["MP4Box", "-add", f"{input_file}#video", "-add", f"{input_file}#audio3", output_audio3])

    # 2️⃣ Ré-indexer le MP4 pour compatibilité FFmpeg
    fixed_output = f"{base}_fixed{ext}"
    run(["MP4Box", "-inter", "500", output_audio3, "-out", fixed_output])

    # 3️⃣ Appeler le script de traduction sur le MP4 fixé
    run(["python", "traduire_video.py", fixed_output])

    print("\n✅ Traitement terminé. Fichier prêt :", fixed_output)

if __name__ == "__main__":
    main()
