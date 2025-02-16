from text2video.tts_with_emotion import EmotionAwareTortoiseTTS

# Create an instance of the class
tts_engine = EmotionAwareTortoiseTTS()

lines = ["The founding of Rome is steeped in mythological drama that captured imaginations for millennia.",
         "The tale begins with twin brothers Romulus and Remus, supposedly descendants of the Trojan hero Aeneas, being abandoned as infants and miraculously nursed by a she-wolf.",
         "After growing up as shepherds, they decided to establish a city but disagreed on its location."
         "Romulus chose the Palatine Hill, while Remus preferred the Aventine Hill."]
config = {
    "tts_settings": {
        "voice": "freeman",
        "preset": "fast",
        "sample_rate": 24000
    }
}
out_dir = "./outputs_tts"

tts_engine.generate_tts(lines, config, out_dir)