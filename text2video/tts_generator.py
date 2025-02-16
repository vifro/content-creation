import os
import torchaudio
import tortoise

from tortoise.utils.audio import load_voices
from tortoise.api import TextToSpeech

def generate_tts(lines: list, config: dict, out_dir: str):
    """
    Generate TTS for each line using the specified voice & preset.
    """
    tts_settings = config.get("tts_settings", {})
    voice = tts_settings.get("voice", "freeman")
    preset = tts_settings.get("preset", "fast")
    sample_rate = tts_settings.get("sample_rate", 24000)

    tts = TextToSpeech()
    # Tortoise includes some sample voices internally
    voices_data = load_voices([voice])
    voice_samples, conditioning_latents = voices_data

    for i, line in enumerate(lines, start=1):
        out_file = os.path.join(out_dir, f"line_{i}.wav")
        print(f"[INFO] Generating audio {i}/{len(lines)}: {line}")
        gen_audio = tts.tts_with_preset(
            line,
            voice_samples=voice_samples,
            conditioning_latents=conditioning_latents,
            preset=preset
        )
        torchaudio.save(out_file, gen_audio.squeeze(0).cpu(), sample_rate)
        print(f"[INFO] Saved {out_file}")
