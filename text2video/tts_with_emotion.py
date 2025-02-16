import os
import torchaudio
import torch
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voices

# For emotion classification
from transformers import pipeline

class EmotionAwareTortoiseTTS:
    """
    A class to generate TTS using Tortoise with optional emotion-based adjustments.
    The generate_tts() method has the same signature as your original function:
        generate_tts(lines: list, config: dict, out_dir: str)
    """

    def __init__(self, emotion_model_name: str = "bhadresh-savani/distilbert-base-uncased-emotion"):
        """
        :param emotion_model_name: Name of the Hugging Face model used for emotion classification.
        """
        # 1. Initialize Tortoise once
        print("[INFO] Initializing Tortoise TTS...")
        self.tts = TextToSpeech()  # can add Tortoise init params for optimization if desired

        # 2. Initialize the emotion classifier (only once)
        print(f"[INFO] Loading emotion classifier: {emotion_model_name}")
        self.emotion_classifier = pipeline(
            "text-classification",
            model=emotion_model_name,
            return_all_scores=True
        )
        print("[INFO] Initialization complete.")

    def generate_tts(self, lines: list, config: dict, out_dir: str):
        """
        Generate TTS for each line using the specified voice & preset.
        Includes emotion analysis to adjust the prompt text for expressive output.
        Output files: line_1.wav, line_2.wav, etc.
        """
        # Extract TTS settings
        tts_settings = config.get("tts_settings", {})
        voice = tts_settings.get("voice", "freeman")
        preset = tts_settings.get("preset", "fast")
        sample_rate = tts_settings.get("sample_rate", 24000)

        # Load the chosen voice samples & conditioning latents (once)
        print(f"[INFO] Loading voice '{voice}' for Tortoise TTS...")
        voice_samples, conditioning_latents = load_voices([voice])

        print("[INFO] Starting emotion-aware TTS generation...")

        # Classify the emotion for each line in a batch
        # The classifier can accept a list of texts. We'll parse out top emotions for each.
        # Each item in `results` is a list of dicts: [{'label': 'anger', 'score': 0.02}, ...]
        if lines:
            results = self.emotion_classifier(lines)
        else:
            results = []

        for i, line in enumerate(lines, start=1):
            out_file = os.path.join(out_dir, f"line_{i}.wav")
            print(f"[INFO] Generating audio {i}/{len(lines)}: {line}")

            # 1. Figure out the top emotion for this line
            emotion_scores = results[i-1]  # the i-th line's result
            # Sort by score descending
            emotion_scores_sorted = sorted(emotion_scores, key=lambda x: x['score'], reverse=True)
            top_emotion = emotion_scores_sorted[0]['label']  # e.g. 'joy', 'sadness', etc.
            print(f"    Detected emotion: {top_emotion} (score={emotion_scores_sorted[0]['score']:.3f})")

            # 2. Prepare text with optional emotion cues
            prompt_text = self._prepare_prompt_with_emotion(line, top_emotion)

            # 3. Generate audio using Tortoise TTS
            with torch.no_grad():
                gen_audio = self.tts.tts_with_preset(
                    text=prompt_text,
                    voice_samples=voice_samples,
                    conditioning_latents=conditioning_latents,
                    preset=preset
                )

            # 4. Save the audio
            torchaudio.save(out_file, gen_audio.squeeze(0).cpu(), sample_rate)
            print(f"[INFO] Saved {out_file}")

        print("[INFO] All lines processed.")

    def _prepare_prompt_with_emotion(self, text: str, emotion: str) -> str:
        """
        Modify the text to cue Tortoise for emotional expression.
        (Prompt engineering approach: bracketed text, punctuation, etc.)
        """
        # You can customize these phrases or logic depending on how Tortoise
        # interprets bracketed text. For example, "I'm angry" or "In a sad tone," etc.
        # Tortoise won't read bracketed text out loud, but uses it as style context.
        # If you're using a Tortoise variant that doesn't interpret bracketed text,
        # you might instead do something with punctuation or comedic stylization.
        if emotion.lower() == "joy":
            # e.g.: [Happy tone], or [Speaking joyfully],
            return f"[Speaking joyfully,] {text}"
        elif emotion.lower() in ["anger", "angry"]:
            return f"[I am angry,] {text}"
        elif emotion.lower() == "sadness":
            return f"[I am sad,] {text}"
        elif emotion.lower() == "fear":
            return f"[I am fearful,] {text}"
        elif emotion.lower() == "surprise":
            return f"[I am surprised,] {text}"
        else:
            # Default or neutral tone
            return text
