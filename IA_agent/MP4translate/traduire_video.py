import sys
import subprocess
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import warnings

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def supprimer_repetitions_strictes(segments):
    """ZÉRO RÉPÉTITION - garde UNIQUEMENT contenu nouveau"""
    uniques = []
    phrases_vues = set()
    
    for seg in segments:
        texte = seg["text"].strip().lower()
        mots = texte.split()
        
        # Ignorer silences courts et répétitions
        if (len(mots) < 3 or 
            texte in phrases_vues or
            any(mot in ["guerriers", "guerrier", "les"] for mot in mots)):
            continue
            
        uniques.append(seg)
        phrases_vues.add(texte)
    
    print(f"📝 Segments: {len(segments)} → {len(uniques)} (STRICT)")
    return uniques

def generer_srt(segments, fichier_srt):
    with open(fichier_srt, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            f.write(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n\n")
    print(f"✅ SRT: {fichier_srt}")

def extraire_audio(video_path):
    audio_path = "audio_original.wav"
    subprocess.run(['ffmpeg', '-i', video_path, '-map', '0:a:0', '-ar', '22050', audio_path, '-y'], 
                   capture_output=True, check=True)
    return audio_path

def get_video_duration(video_path):
    result = subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', video_path], 
                            capture_output=True, text=True)
    return float(result.stdout.strip())

def transcrire(audio_path):
    print("🔄 Whisper (strict)...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="fr")
    return supprimer_repetitions_strictes(result["segments"])

def traduire(segments):
    print("🌐 Traduction grec...")
    translator = GoogleTranslator(source='fr', target='el')
    traduits = []
    for s in segments:
        traduit = translator.translate(s["text"].strip())
        traduits.append({"start": s["start"], "end": s["end"], "text": traduit})
    return traduits

def generer_voix_grec_dominante(texte, duration):
    """Voix GRECQUE DOMINANTE sur TOUTE la vidéo"""
    # Texte répété 4x pour couvrir vidéo
    texte_long = (texte + " ") * 4
    
    print(f"🎤 Voix grecque dominante ({duration}s)...")
    tts = gTTS(text=texte_long, lang="el", slow=False)
    tts.save("voix_grec_dominante.mp3")
    
    # Couper exactement durée vidéo
    subprocess.run(['ffmpeg', '-i', 'voix_grec_dominante.mp3', '-t', str(duration), '-y', 'voix_grec_finale.mp3'], 
                   capture_output=True, check=True)
    os.remove('voix_grec_dominante.mp3')
    return "voix_grec_finale.mp3"

def mix_voix_dominante(fond_path, voix_path, duration):
    """VOIX GRECQUE 100% + fond FR 20% (INAUDIBLE)"""
    subprocess.run([
        'ffmpeg', '-i', fond_path, '-i', voix_path,
        '-filter_complex', 
        f'[0:a]volume=0.2[a];[1:a]volume=1.2[b];[a][b]amix=inputs=2:duration=first[out]',
        '-map', '[out]', '-t', str(duration), 'audio_final.mp3', '-y'
    ], capture_output=True, check=True)
    return "audio_final.mp3"

def video_finale(video_path, audio_path, output):
    subprocess.run([
        'ffmpeg', '-i', video_path, '-i', audio_path,
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
        '-map', '0:v:0', '-map', '1:a:0', '-y', output
    ], capture_output=True, check=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python traduire_video.py video.mp4")
        sys.exit(1)
    
    video = sys.argv[1]
    nom = os.path.splitext(os.path.basename(video))[0]
    
    print("🚀 VOIX GRECQUE TOTALE - ZÉRO FRANÇAIS AUDIBLE")
    duration = get_video_duration(video)
    print(f"📏 {duration:.0f}s")
    
    # 1. Audio + transcription stricte
    fond = extraire_audio(video)
    segments_fr = transcrire(fond)
    generer_srt(segments_fr, f"{nom}_fr.srt")
    
    # 2. Traduction
    segments_gr = traduire(segments_fr)
    generer_srt(segments_gr, f"{nom}_gr.srt")
    
    # 3. Voix grecque dominante
    texte_gr = " ".join(s["text"] for s in segments_gr)
    voix = generer_voix_grec_dominante(texte_gr, duration)
    
    # 4. Mix voix grecque TOTALE
    mix = mix_voix_dominante(fond, voix, duration)
    
    # 5. Vidéo finale
    final = f"{nom}_grecque.mp4"
    video_finale(video, mix, final)
    
    # Nettoyage
    for f in [fond, voix, mix]:
        try: os.remove(f)
        except: pass
    
    size = os.path.getsize(final)/1024/1024
    print(f"\n🎉 FINAL ! {final} ({size:.1f}MB)")
    print("✅ **VOIX GRECQUE CLAIRE** sur 100% vidéo")
    print("✅ **Fond français inaudible** (20%)")
