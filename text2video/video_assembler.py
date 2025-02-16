import os
from moviepy import (
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)

def assemble_video(prompts, lines, config, base_out_dir, video_path):
    """
    Combine images (in 'images' folder) and audio (in 'audio' folder)
    into a final video using MoviePy.
    """
    images_dir = os.path.join(base_out_dir, "images")
    audio_dir = os.path.join(base_out_dir, "audio")

    video_cfg = config.get("video_settings", {})
    fps = video_cfg.get("fps", 24)
    font_path = video_cfg.get("font_path", None)
    font_size = video_cfg.get("font_size", 24)
    text_color = video_cfg.get("text_color", "white")
    text_position = video_cfg.get("text_position", ("center", "bottom"))

    clips = []
    for i, line in enumerate(lines, start=1):
        img_file = os.path.join(images_dir, f"frame_{i}.png")
        audio_file = os.path.join(audio_dir, f"line_{i}.wav")

        if not os.path.isfile(img_file) or not os.path.isfile(audio_file):
            print(f"[WARN] Missing file for line {i}: {img_file} or {audio_file}")
            continue

        image_clip = ImageClip(img_file)
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        image_clip = image_clip.with_duration(duration).with_audio(audio_clip)

        # optionally add text
        txt_clip = TextClip(
            text=line,
            font_size=font_size,
            font=font_path,
            color=text_color,
            method='caption',
            size=(image_clip.w - 100, None)
        ).with_duration(duration).with_position(text_position)

        final_clip = CompositeVideoClip([image_clip, txt_clip])
        clips.append(final_clip)

    if not clips:
        print("[ERROR] No valid clips to assemble.")
        return

    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile(video_path, fps=fps)
