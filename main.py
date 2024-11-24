from elevenlabs import ElevenLabs

from secrets import API_KEY

elevenlabs = ElevenLabs(api_key=API_KEY)


def generate_sound_effect(text: str, output_path: str):
    print("Generating sound effects...")

    result = elevenlabs.text_to_sound_effects.convert(
        text=text,
        # duration_seconds=12,
        prompt_influence=0.5,  # Optional, if not provided will use the default value of 0.3
    )

    with open(output_path, "wb") as f:
        for chunk in result:
            f.write(chunk)

    print(f"Audio saved to {output_path}")


if __name__ == "__main__":
    generate_sound_effect("alien voice", "output.mp3")
