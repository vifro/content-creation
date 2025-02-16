import transformers
import diffusers
print(f"Transformers version: {transformers.__version__}")
print(f"Diffusers version: {diffusers.__version__}")


import yaml
import torch
from diffusers import StableDiffusionXLPipeline



# 1. Load the prompt schema from a YAML file (you can also hardcode this into a dict)
def load_schema(schema_path: str):
    with open(schema_path, "r") as f:
        data = yaml.safe_load(f)
    return data

# 2. Build a helper function to assemble the final prompt for each scene
def build_prompt(scene_description: str, schema: dict, extra_scene_override: str = None) -> str:
    """
    Combine the global style attributes, any override, and the scene description
    into a single text prompt for Stable Diffusion.
    """
    style = schema["series_style"]
    art_style = style["art_style"]
    color_palette = style["color_palette"]
    mood = style["mood"]

    # If there's an override key (like "Stormy"), find its details
    overrides = schema.get("scene_overrides", [])
    override_text = ""
    if extra_scene_override:
        for ov in overrides:
            if ov["key"] == extra_scene_override:
                override_text = f", {ov['details']}"
                break

    # Combine everything into a descriptive line
    # Example: "A painting of Romulus and Remus with a she-wolf, classical painting, warm earthy tones..."
    base_prompt = (
        f"{scene_description}, {art_style}, {color_palette}, {mood}{override_text}"
    )
    return base_prompt

def main():
    # 3. Load schema
    schema_path = "roman_prompt_schema.yaml"  # adjust path to where your YAML is
    schema = load_schema(schema_path)
    negative = schema["series_style"]["negative_prompt"]

    # 4. Initialize the Stable Diffusion pipeline
    # For SDXL base model:
    #   "stabilityai/stable-diffusion-xl-base-1.0"
    # Alternatively, pick a fine-tuned model from HF
    base = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16
    )
    base.to("cuda")
    refiner = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-refiner-1.0",
        text_encoder_2=base.text_encoder_2,
        vae=base.vae,
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16",
    )
    refiner.to("cuda")

    # (Optional) If you have a refiner for SDXL:
    # refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    #     "stabilityai/stable-diffusion-xl-refiner-1.0",
    #     torch_dtype=torch.float16
    # )
    # refiner.to("cuda")
    # We'll skip that for MVP

    # 5. Example scenes from your Roman Kingdom segment
    scenes = [
        "Romulus and Remus being nursed by a fierce she-wolf in an ancient forest clearing",
        "Romulus kills Remus near the new city walls in a moment of tragic conflict",
        "Romulus presides over the first Roman Senate, establishing early Roman institutions",
        "Romans abduct women from neighboring tribes - the Sabine Women - leading to conflict",
        "Romulus disappears in a sudden thunderstorm, ascending to godhood in mythic fashion"
    ]

    # 6. Generate each image
    for i, scene_desc in enumerate(scenes, start=1):
        # For example, you could choose an override like "Stormy" if your scene is dramatic
        # but here let's keep it None or your own logic:
        override_key = None
        if "thunderstorm" in scene_desc.lower():
            override_key = "Stormy"

        prompt = build_prompt(scene_desc, schema, extra_scene_override=override_key)

        # Define how many steps and what % of steps to be run on each experts (80/20) here
        n_steps = 40
        high_noise_frac = 0.8

        # 7. Run inference
        print(f"negative: {negative}")
        print(f"[INFO] Generating image {i} with prompt: {prompt}")
        image = base(
            prompt,
            negative_prompt=negative,
            num_inference_steps=50,
            guidance_scale=7.5 , # tweak as desired,
            cross_attention_kwargs = {"scale": 1.0},  # Add this line
            added_cond_kwargs={},  # Empty dict is safe
            output_type="latent"
        )
        image = refiner(
            prompt=prompt,
            num_inference_steps=n_steps,
            denoising_start=high_noise_frac,
            image=image
        )

        # 8. Save the image
        out_name = f"data/images/roman_kingdom_{i}.png"
        image.save(out_name)
        print(f"[INFO] Saved {out_name}")

if __name__ == "__main__":
    main()
