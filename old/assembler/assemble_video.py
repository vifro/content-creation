import os
from moviepy import (
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)

def main():
    # 1. We assume the same number of images and audio files, matched by index.
    images_dir = "data/images"  # Directory containing images
    audio_dir = "data/speech"   # Directory containing audio files
    output_video = "data/movie/final_roman_kingdom.mp4"

    # 2. Scenes / lines
    scenes = [
        {
            "image": "roman_kingdom_1.png",
            "audio": "tts_1.wav",
            "text": "Romulus and Remus are nursed by a fierce she-wolf in an ancient forest clearing."
        },
        {
            "image": "roman_kingdom_2.png",
            "audio": "tts_2.wav",
            "text": "Romulus kills Remus near the new city walls in a moment of tragic conflict."
        },
        {
            "image": "roman_kingdom_3.png",
            "audio": "tts_3.wav",
            "text": "Romulus presides over the first Roman Senate, establishing early Roman institutions."
        },
        {
            "image": "roman_kingdom_4.png",
            "audio": "tts_4.wav",
            "text": "Romans abduct the Sabine women, leading to war and eventual integration."
        },
        {
            "image": "roman_kingdom_5.png",
            "audio": "tts_5.wav",
            "text": "Romulus disappears in a sudden thunderstorm, ascending to godhood in mythic fashion."
        }
    ]
    font_path = "/usr/share/fonts/opentype/Kanok-4nY5p.otf"

    clips = []
    for scene in scenes:
        img_path = os.path.join(images_dir, scene["image"])
        aud_path = os.path.join(audio_dir, scene["audio"])
        caption_text = scene["text"]

        # 3. Create an ImageClip
        image_clip = ImageClip(img_path)

        # 4. Load audio
        audio_clip = AudioFileClip(aud_path)
        # Set the clip's duration to match the audio length
        image_clip = image_clip.with_duration(audio_clip.duration)

        # 5. Attach the audio to the image clip
        image_clip = image_clip.with_audio(audio_clip)

        # 6. Create a caption (subtitles) TextClip
        txt_clip = TextClip(
            text=caption_text,
            font=font_path,
            font_size=24,
            color='white',
            size=(image_clip.w - 100, None),  # wrap text
            method='caption'
        ).with_position(("center", "bottom")).with_duration(audio_clip.duration)

        # 7. Combine image and text
        final_scene_clip = CompositeVideoClip([image_clip, txt_clip])

        clips.append(final_scene_clip)

    # 8. Concatenate clips
    final_video = concatenate_videoclips(clips, method="compose")

    # 9. Write final video
    final_video.write_videofile(output_video, fps=24)
    print(f"[INFO] Video saved to {output_video}")

if __name__ == "__main__":
    main()
