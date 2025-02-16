# Text2Video: Modular CLI Pipeline for Generating Videos from Text

This project demonstrates a **modular pipeline** for turning a plain text script into a video featuring:
- **AI-generated images** (via Stable Diffusion)
- **Synthesized audio** narration (via TTS)
- **Assembly** into a final video (via MoviePy)

---

## Features

1. **CLI Interface**: Simple to run end-to-end or individual steps.
2. **Modular Design**: Separate modules for text parsing, prompt building, image creation, TTS, and video assembly.
3. **YAML Config**: Centralized configuration for style, voice, and other settings.
4. **Clean Output Folders**: Organized output in a folder named after the text title.

---

## Quickstart

1. **Create a Python environment** (optional):
```bash
   conda create -n text2video python=3.9
   conda activate text2video
```
Or use virtualenv if you prefer.

```commandline
pip install -r requirements.txt
```

If you encounter version mismatches, pin the versions of transformers, diffusers, and huggingface_hub to compatible ones.

```bash
# (A) Generate a default config and exit:
python -m text2video.cli --input /path/to/story.txt --generate-config

# (B) Run the full pipeline with the config from step A:
python -m text2video.cli --input /path/to/story.txt --config /path/to/default_config.yaml
```

This will:

1. Parse the text file into lines or sentences
2. Generate prompts from the lines using the config
3. Create images for each prompt (Stable Diffusion)
4. Synthesize TTS audio for each line
5. Combine images and audio into a video
View the Results:
1. A folder named after your text’s title (or filename) will be created.
2. Inside are subfolders: images/, audio/, and video/.
3. The final video (e.g. my_text.mp4) is located under video/.

4. CLI Options
--input: Path to the input .txt file (required).
--config: Path to a YAML config file (default uses built-in config).
--output: Custom output folder name (otherwise uses text’s title).
--generate-config: Generate a default YAML config for the input text, then exit.
--skip-images: Skip image generation (if you already have them).
--skip-tts: Skip TTS generation (if you already have the audio).
--skip-video: Skip final video assembly (if you only want images/audio).


python -m text2video.cli --input story.txt --generate-config
