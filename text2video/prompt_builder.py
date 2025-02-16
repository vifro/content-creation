def build_prompts(lines: list, config: dict) -> list:
    """
    For each line, build a prompt combining the line with the
    'prompt_style' parameters (art_style, color_palette, mood).
    """
    style_cfg = config.get("prompt_style", {})
    art_style = style_cfg.get("art_style", "")
    color_palette = style_cfg.get("color_palette", "")
    mood = style_cfg.get("mood", "")

    prompts = []
    for line in lines:
        prompt = f"{line}, {art_style}, {color_palette}, {mood}"
        prompts.append(prompt)
    return prompts
