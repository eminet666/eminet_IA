# audio_generator.py
# Génération de l'audio avec edge-tts

import os
import asyncio
import tempfile
import edge_tts
from pydub import AudioSegment
from config import VOICES, PAUSE_DURATION


async def generate_audio_from_dialogue_async(dialogue_lines, output_file="dialogue.mp3"):
    """
    Génère un fichier audio MP3 à partir des répliques du dialogue
    avec edge-tts pour des voix grecques naturelles
    """
    if not dialogue_lines:
        print("⚠️  Aucune réplique trouvée dans le dialogue")
        return None
    
    print(f"- Génération audio de {len(dialogue_lines)} répliques avec edge-tts...")
    audio_segments = []
    
    # Créer un dossier temporaire pour les fichiers audio
    with tempfile.TemporaryDirectory() as temp_dir:
        for i, (speaker, text) in enumerate(dialogue_lines):
            try:
                voice = VOICES[speaker]
                temp_file = os.path.join(temp_dir, f"temp_{i}_{speaker}.mp3")
                
                # Générer l'audio avec edge-tts
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(temp_file)
                
                # Charger avec pydub
                audio = AudioSegment.from_mp3(temp_file)
                
                # Ajouter l'audio
                audio_segments.append(audio)
                
                # Ajouter une pause entre les répliques
                pause = AudioSegment.silent(duration=PAUSE_DURATION)
                audio_segments.append(pause)
                
                print(f"  ✓ Réplique {i+1}/{len(dialogue_lines)} - {speaker}")
                
            except Exception as e:
                print(f"  ✗ Erreur pour la réplique {i+1}: {e}")
                continue
        
        if not audio_segments:
            print("⚠️  Aucun segment audio généré")
            return None
        
        # Combiner tous les segments
        print("- Assemblage des segments audio...")
        final_audio = sum(audio_segments)
        
        # Exporter le fichier final
        final_audio.export(output_file, format="mp3")
        print(f"✓ Audio généré : {output_file} ({len(final_audio)/1000:.1f}s)")
    
    return output_file


def generate_audio_from_dialogue(dialogue_lines, output_file="dialogue.mp3"):
    """
    Wrapper synchrone pour la fonction asynchrone
    """
    return asyncio.run(generate_audio_from_dialogue_async(dialogue_lines, output_file))