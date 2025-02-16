#!/usr/bin/env python3
import argparse
import os
import sys
from text2video.tts_with_emotion import EmotionAwareTortoiseTTS


from text2video.config import load_config, save_config, generate_default_config
from text2video.text_parser import parse_text_file
from text2video.prompt_builder import build_prompts
from text2video.image_generator import generate_images
from text2video.tts_generator import generate_tts
from text2video.video_assembler import assemble_video
from text2video.utils import get_title_slug


def main():
    parser = argparse.ArgumentParser(
        description="Convert a text file into a video with AI-generated images and audio."
    )
    parser.add_argument("--input", type=str, required=True,
                        help="Path to the input text file.")
    parser.add_argument("--config", type=str, default=None,
                        help="Path to YAML config file. If omitted, default config is used.")
    parser.add_argument("--output", type=str, default=None,
                        help="Optional output folder name. Defaults to slugified text title.")
    parser.add_argument("--generate-config", action="store_true",
                        help="Generate a default config file based on the input text and exit.")
    parser.add_argument("--skip-images", action="store_true",
                        help="Skip image generation step.")
    parser.add_argument("--skip-tts", action="store_true",
                        help="Skip TTS audio generation step.")
    parser.add_argument("--skip-video", action="store_true",
                        help="Skip final video assembly step.")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: input file '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # 1. Parse the text to get lines or sentences
    lines, title = parse_text_file(args.input)

    # 2. Determine output directory
    if args.output:
        out_dir = args.output
    else:
        out_dir = get_title_slug(title)  # e.g., "My_Story"
    os.makedirs(out_dir, exist_ok=True)

    # 3. Handle config
    if args.generate_config:
        default_config = generate_default_config(title)
        config_path = os.path.join(out_dir, "default_config.yaml")
        save_config(default_config, config_path)
        print(f"[INFO] Default config saved to: {config_path}")
        sys.exit(0)

    if args.config and os.path.isfile(args.config):
        config = load_config(args.config)
    else:
        config = generate_default_config(title)
        print("[INFO] Using built-in default config (no --config provided or file not found).")

    # 4. Build final prompts for each line
    prompts = build_prompts(lines, config)

    # 5. (Optional) Generate images
    if not args.skip_images:
        images_dir = os.path.join(out_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        generate_images(prompts, config, images_dir)

    # 6. (Optional) Generate TTS
    if not args.skip_tts:
        audio_dir = os.path.join(out_dir, "audio")
        os.makedirs(audio_dir, exist_ok=True)
        # Create an instance of the class
        tts_engine = EmotionAwareTortoiseTTS()
        tts_engine.generate_tts(lines, config, audio_dir)

    # 7. (Optional) Assemble the video
    if not args.skip_video:
        video_dir = os.path.join(out_dir, "video")
        os.makedirs(video_dir, exist_ok=True)
        video_path = os.path.join(video_dir, f"{get_title_slug(title)}.mp4")
        assemble_video(prompts, lines, config, out_dir, video_path)
        print(f"[INFO] Final video saved at: {video_path}")


if __name__ == "__main__":
    main()
