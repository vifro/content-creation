import yaml
import os

def load_config(path: str) -> dict:
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config

def save_config(config: dict, path: str):
    with open(path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

def generate_default_config(title: str) -> dict:
    """
    Build a default YAML config dictionary, which can be saved or
    updated by the user.
    """
    config = {
        "project_title": title,
        "image_settings": {
            "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
            "refiner_id": "stabilityai/stable-diffusion-xl-refiner-1.0",
            "guidance_scale": 7.5,
            "num_inference_steps": 50,
            "negative_prompt": "text watermark, lowres, bad anatomy, low quality"
        },
        "prompt_style": {
            "art_style": "Artistic and classical painting",
            "color_palette": "warm earthy tones",
            "mood": "epic and majestic"
        },
        "tts_settings": {
            "voice": "freeman",
            "preset": "fast",
            "sample_rate": 24000
        },
        "video_settings": {
            "fps": 24,
            "font_path": "/usr/share/fonts/opentype/Kanok-4nY5p.otf",
            "font_size": 24,
            "text_color": "white",
            "text_position": ("center", "bottom")
        }
    }
    return config
