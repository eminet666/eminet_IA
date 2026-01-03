import subprocess
import json
import sys

def lister_pistes_audio_ffprobe(chemin_fichier):
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_format', '-show_streams', chemin_fichier
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    print(f"Fichier: {chemin_fichier}")
    for stream in data['streams']:
        if stream['codec_type'] == 'audio':
            print(f"Piste audio ID {stream['index']}: {stream['codec_name']}")
            print(f"  Langue: {stream.get('tags', {}).get('language', 'Non spécifiée')}")
            print(f"  Canaux: {stream['channels']}")
            print("---")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py votre_video.mp4")
        sys.exit(1)
    
    fichier = sys.argv[1]
    lister_pistes_audio_ffprobe(fichier)
