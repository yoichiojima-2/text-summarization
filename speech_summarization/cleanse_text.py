import os
from pathlib import Path

from openai import OpenAI


def cleanse_texts(input_dir: str):
    for f in Path(input_dir).rglob("*"):
        if f.is_file():
            cleanse_text(f)


def cleanse_text(input_path: str):
    prompt = (
        "I have a transcript generated by Whisper that contains repeated phrases "
        "and sentences which were not present in the original audio. "
        "The text is in Japanese, a language that often doesn't use spaces or "
        "punctuation in the same way as English, making it challenging to identify "
        "and remove these repetitions. I need your help to clean up this transcript "
        "by removing any repeated content without altering the original meaning "
        "or omitting important information. Please ensure the cleaned-up version "
        "maintains a natural and coherent flow, suitable for professional use. "
        "Below is the transcript. Please process it and provide a version with "
        "the repetitions removed."
        "Please provide the cleaned-up version of the following transcript with "
        "unnecessary repetitions removed, ensuring the text remains coherent "
        "and true to the original content. "
        "also, I would like you to remove unnecessary spaces and newlines."
    )

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    input_path = Path(input_path)
    input_text = input_path.read_text()

    response = (
        client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt},
                {"role": "user", "content": input_text},
            ],
            model="gpt-4",
        )
        .choices[0]
        .message.content
    )

    print(f"response: {response}")

    target_dir = Path("./data/cleanse_text") / input_path.parts[-2]
    target_dir.mkdir(parents=True, exist_ok=True)
    output_filename = input_path.name.replace("splitted", "cleansed")
    (target_dir / output_filename).write_text(response)
