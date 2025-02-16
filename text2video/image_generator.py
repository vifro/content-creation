import torch
from diffusers import DiffusionPipeline

def generate_images(prompts: list, config: dict, out_dir: str):
    """
    Use StableDiffusionXLPipeline to generate images for each prompt.
    """
    # 1. Load models
    image_settings = config.get("image_settings", {})
    model_id = image_settings.get("model_id")
    refiner_id = image_settings.get("refiner_id")
    negative_prompt = image_settings.get("negative_prompt", "")
    guidance_scale = image_settings.get("guidance_scale", 7.5)
    num_inference_steps = image_settings.get("num_inference_steps", 50)

    base = DiffusionPipeline.from_pretrained(
        model_id, torch_dtype=torch.float16
    ).to("cuda")

    refiner = DiffusionPipeline.from_pretrained(
        refiner_id,
        text_encoder_2=base.text_encoder_2,
        vae=base.vae,
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16",
    ).to("cuda")

    # 2. For each prompt, generate an image and save
    for i, prompt in enumerate(prompts, start=1):
        print(f"[INFO] Generating image {i}/{len(prompts)}: {prompt}")
        # base pass
        image_latent = base(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            output_type="latent"
        ).images

        # refine pass
        refined = refiner(
            prompt=prompt,
            image=image_latent
        ).images[0]

        out_path = f"{out_dir}/frame_{i}.png"
        refined.save(out_path)
        print(f"[INFO] Saved {out_path}")
