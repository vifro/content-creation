#!/usr/bin/env python3

import os
import torchaudio
import tortoise
import os
# Tortoise-specific imports
from tortoise.utils.audio import load_audio, load_voices
from tortoise.api import TextToSpeech


def main():

    print(f"current dir: {os.getcwd()}")
    voices_dir = os.path.join(os.path.dirname(tortoise.__file__), "voices")
    print("Voices directory:", voices_dir)
    print("Available voices:", os.listdir(voices_dir))

    # 1. Define the lines you want to synthesize (matching your images)
    #    You can load from a file or keep them inline for an MVP.
    transcript_lines = [
        "Romulus and Remus are nursed by a fierce she-wolf in an ancient forest clearing.",
        "Romulus kills Remus near the new city walls in a moment of tragic conflict.",
        "Romulus presides over the first Roman Senate, establishing early Roman institutions.",
        "Romans abduct the Sabine women, leading to war and eventual integration.",
        "Romulus disappears in a sudden thunderstorm, ascending to godhood in mythic fashion."
    ]

    # Initialize Tortoise
    tts = TextToSpeech()

    # Load the built-in 'train_yard' voice from Tortoise’s sample library
    voices_data = load_voices(["freeman"])
    print("Voices data:", voices_data)
    voice_samples, conditioning_latents = voices_data

    output_dir = "data/speech/"
    os.makedirs(output_dir, exist_ok=True)

    for i, line in enumerate(transcript_lines, start=1):
        out_path = os.path.join(output_dir, f"tts_{i}.wav")
        print(f"[INFO] Generating audio for line {i}: {line}")

        # Pass the samples/latents to tts_with_preset
        gen_audio = tts.tts_with_preset(
            line,
            voice_samples=voice_samples,
            conditioning_latents=conditioning_latents,
            preset="fast",  # or 'standard', 'high_quality'
        )

        # Tortoise returns a tensor, so save with torchaudio
        torchaudio.save(out_path, gen_audio.squeeze(0).cpu(), 24000)
        print(f"[INFO] Saved {out_path}")

    print("[INFO] TTS generation complete!")


if __name__ == "__main__":
    main()

