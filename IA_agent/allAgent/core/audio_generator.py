# core/audio_generator.py
# Génération audio avec edge-tts — moteur générique

import os
import asyncio
import tempfile
import edge_tts
from pydub import AudioSegment


async def _generate_async(lines, lang, output_file):
    """
    Génère le fichier MP3 de façon asynchrone.
    Vitesse et pause sont lues depuis lang.AUDIO_RATE et lang.PAUSE_DURATION.
    """
    if not lines:
        print("Aucune réplique trouvée")
        return None

    print(f"- Génération audio : {len(lines)} répliques (vitesse : {lang.AUDIO_RATE})...")
    segments = []

    with tempfile.TemporaryDirectory() as tmp:
        for i, (speaker, text) in enumerate(lines):
            try:
                voice    = lang.CHARACTERS[speaker]["voice"]
                tmp_file = os.path.join(tmp, f"tmp_{i}.mp3")

                await edge_tts.Communicate(text, voice, rate=lang.AUDIO_RATE).save(tmp_file)

                segments.append(AudioSegment.from_mp3(tmp_file))
                segments.append(AudioSegment.silent(duration=lang.PAUSE_DURATION))

                print(f"  ok {i+1}/{len(lines)} — {speaker}")

            except Exception as e:
                print(f"  erreur réplique {i+1} : {e}")
                continue

    if not segments:
        print("Aucun segment audio généré")
        return None

    print("- Assemblage des segments...")
    final = sum(segments)
    final.export(output_file, format="mp3")
    print(f"ok Audio : {output_file} ({len(final)/1000:.1f}s)")
    return output_file


def generate_audio(lines, lang, output_file):
    """Wrapper synchrone"""
    return asyncio.run(_generate_async(lines, lang, output_file))
