import torch
import random
import os
import yaml
import re

from TTS.api import TTS


def load_config():
    with open("tts_config.yml", "r") as file:
        return yaml.safe_load(file)


def init_tts():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


def print_status(id, samples):
    samples_str = ", ".join(map(str, samples))
    message = f"Generating #{id} with {samples_str}"
    print(message)
    with open("log.txt", "a") as f:
        f.write(message + "\n")


def find_last_id():
    return max(
        [
            int(re.search(r"_(\d+)\.", f).group(1))
            for f in os.listdir("output")
            if re.search(r"_(\d+)\.", f)
        ],
        default=0,
    )


if __name__ == "__main__":
    config = load_config()

    if config.get("shuffle", False):
        samples = random.shuffle(config["samples"])
    else:
        samples = config["samples"]

    last_id = find_last_id()

    tts = init_tts()

    itr = 0
    while itr < config["iterations"]:
        for i in range(len(samples)):
            sample_files = ["samples/{}.wav".format(sample) for sample in samples[i]]
            id = last_id + itr + 1
            print_status(id, samples)
            tts.tts_to_file(
                text=config["text"],
                speaker_wav=sample_files,
                file_path="output/output_{}.wav".format(id),
                language="en",
                split_sentences=False,
            )
            itr += 1
