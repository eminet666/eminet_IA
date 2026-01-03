import sys
import os
import subprocess
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
import warnings

# On ignore les warnings non critiques
warnings.filterwarnings("ignore")

def format_timestamp(seconds):
    """Formate les secondes en format SRT (00:00:00,000)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generer_srt(segments, fichier_srt):
    """Génère un fichier de sous-titres .srt"""
    with open(fichier_srt, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            text = seg["text"].strip()
            if text:
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
    print(f"📝 SRT généré : {fichier_srt}")

def speed_change(sound, speed=1.0):
    """Accélère l'audio sans changer la hauteur (pitch)"""
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def generer_audio_double(segments, duree_totale_video):
    """
    Génère une piste audio WAV qui fait EXACTEMENT la durée de la vidéo.
    """
    print(f"🎙️ Génération audio (Dubbing) - Cible stricte : {duree_totale_video:.2f}s")
    
    if duree_totale_video <= 0:
        duree_totale_video = 10.0 # Sécurité

    # Durée cible en millisecondes
    target_duration_ms = int(duree_totale_video * 1000)
    
    # On crée un silence de la longueur exacte de la vidéo
    final_audio = AudioSegment.silent(duration=target_duration_ms)
    temp_file = "temp_segment.mp3"
    
    for i, seg in enumerate(segments):
        text = seg["text"]
        start_ms = int(seg["start"] * 1000)
        end_ms = int(seg["end"] * 1000)
        duration_slot = end_ms - start_ms 
        
        if not text.strip(): continue

        try:
            # Génération TTS
            tts = gTTS(text=text, lang="el", slow=False)
            tts.save(temp_file)
            segment_audio = AudioSegment.from_mp3(temp_file)
            seg_duration = len(segment_audio)
            
            # Vérification et ajustement de la vitesse
            # On ajoute une petite marge (500ms) pour que ça respire
            ratio = seg_duration / (duration_slot + 500)
            
            if ratio > 1.0:
                speed_factor = min(ratio, 1.5) # On limite l'accélération à x1.5
                segment_audio = speed_change(segment_audio, speed_factor)
            
            # Superposition sur la piste principale
            final_audio = final_audio.overlay(segment_audio, position=start_ms)
            
        except Exception as e:
            print(f"⚠️ Segment {i} ignoré : {e}")

    # Nettoyage fichier temp
    if os.path.exists(temp_file):
        os.remove(temp_file)

    # ✂️ TRONCATURE / REMPLISSAGE FINAL ✂️
    # C'est l'étape clé pour que '-c:v copy' fonctionne :
    # Si l'audio est trop long (débordement), on coupe net à la fin de la vidéo.
    # Si trop court, le silence créé au début comble le vide.
    final_audio = final_audio[:target_duration_ms]
    
    # Export en WAV (Format brut, plus sûr pour FFmpeg que le MP3)
    output_audio = "audio_grec_final.wav"
    final_audio.export(output_audio, format="wav")
    
    print(f"📊 Audio WAV calibré prêt : {output_audio}")
    return output_audio

def assembler_video_remplacement(video_path, audio_path, output_path):
    """
    Assemble la vidéo finale :
    1. Tente une COPIE VIDEO (-c:v copy) -> Instantané, qualité originale.
    2. Si échec, bascule sur un RÉENCODAGE (-c:v libx264).
    """
    print("🎬 Assemblage final : Remplacement de la piste audio...")
    
    if not os.path.exists(audio_path):
        print("❌ Erreur : Audio manquant")
        return

    # --- TENTATIVE 1 : COPIE (Rapide) ---
    cmd_copy = [
        'ffmpeg', 
        '-i', video_path,       # Input 0: Vidéo source
        '-i', audio_path,       # Input 1: Audio WAV grec
        '-c:v', 'copy',         # Copie du flux vidéo (sans réencodage)
        '-c:a', 'aac',          # Encodage de l'audio WAV en AAC
        '-b:a', '192k',
        '-map', '0:v:0',        # On garde la Vidéo du fichier 0
        '-map', '1:a:0',        # On garde l'Audio du fichier 1 (Remplace le FR)
        '-y', output_path
    ]
    
    try:
        print("   Mode: COPIE DIRECTE (Optimisé)...")
        # On capture l'erreur pour pouvoir lancer le plan B si besoin
        subprocess.run(cmd_copy, check=True, stderr=subprocess.PIPE)
        print(f"🎉 SUCCÈS ! Vidéo générée (Mode Copie) : {output_path}")
        return # Si ça marche, on s'arrête là
    except subprocess.CalledProcessError:
        print("⚠️ Le mode Copie a échoué (probablement un souci de timestamps).")
        print("   Basculement automatique vers le mode RÉENCODAGE...")

    # --- TENTATIVE 2 : RÉENCODAGE (Robuste) ---
    cmd_encode = [
        'ffmpeg', 
        '-i', video_path, 
        '-i', audio_path,
        '-c:v', 'libx264',      # Réencodage vidéo
        '-preset', 'fast',      # Rapide
        '-c:a', 'aac', 
        '-b:a', '192k',
        '-map', '0:v:0', 
        '-map', '1:a:0',
        '-shortest',            # Sécurité supplémentaire
        '-pix_fmt', 'yuv420p',
        '-y', output_path
    ]
    
    try:
        subprocess.run(cmd_encode, check=True)
        print(f"🎉 SUCCÈS ! Vidéo générée (Mode Réencodage) : {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ ECHEC TOTAL FFmpeg : {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python traduire_video.py video.mp4")
        sys.exit(1)

    video_input = sys.argv[1]
    
    # Gestion des noms de fichiers
    path_base_no_ext = os.path.splitext(video_input)[0]
    
    print(f"📂 Fichier entrée : {video_input}")
    
    # 1. Récupération de la durée exacte
    try:
        duree_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_input]
        duree_video = float(subprocess.check_output(duree_cmd).strip())
        print(f"⏱️ Durée vidéo exacte : {duree_video}s")
    except:
        print("⚠️ Impossible de lire la durée. Arrêt.")
        sys.exit(1)

    # 2. Extraction Audio Temporaire (Source FR)
    audio_temp_fr = "temp_source_fr.wav"
    subprocess.run(['ffmpeg', '-i', video_input, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', audio_temp_fr, '-y'], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Transcription (Whisper) -> SRT Français
    print("🧠 Transcription (Whisper) en cours...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_temp_fr, language="fr")
    segments_fr = result["segments"]
    
    file_srt_fr = f"{path_base_no_ext}_fr.srt"
    generer_srt(segments_fr, file_srt_fr)
    
    # 4. Traduction -> SRT Grec
    print("🌍 Traduction FR -> GR...")
    translator = GoogleTranslator(source='fr', target='el')
    segments_gr = []
    
    for s in segments_fr:
        try:
            trad = translator.translate(s["text"].strip())
            if trad:
                segments_gr.append({"start": s["start"], "end": s["end"], "text": trad})
        except: pass

    file_srt_gr = f"{path_base_no_ext}_gr.srt"
    generer_srt(segments_gr, file_srt_gr)
    
    # 5. Génération Audio Doublage (Format WAV, Durée stricte)
    audio_grec = generer_audio_double(segments_gr, duree_video)
    
    # 6. Assemblage Final
    output_video = f"{path_base_no_ext}_grec.mp4"
    assembler_video_remplacement(video_input, audio_grec, output_video)
    
    # Nettoyage
    print("🧹 Nettoyage des fichiers temporaires...")
    for f in [audio_temp_fr, audio_grec]:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass

    print("\n--- RAPPORT ---")
    print(f"1. Vidéo Finale : {output_video}")
    print(f"2. Sous-titres FR : {file_srt_fr}")
    print(f"3. Sous-titres GR : {file_srt_gr}")

if __name__ == "__main__":
    main()