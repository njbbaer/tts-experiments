import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

FILES_DIR = "chunk_text/output"
ONLY_NAMES = None  # Ex. ["file1", "file2"]
OUTPUT_DIR = "chapter22"

with open("comfyui_api/body.json", "r") as f:
    prompt = json.load(f)

prompt["36"]["inputs"]["seed"] = 43

files = sorted(os.listdir(FILES_DIR))
for i, file in enumerate(files):
    name = os.path.splitext(file)[0]
    if ONLY_NAMES and name not in ONLY_NAMES:
        continue

    with open(os.path.join(FILES_DIR, file), "r") as text_file:
        prompt["47"]["inputs"]["value"] = text_file.read()
        prompt["37"]["inputs"]["filename_prefix"] = f"audio/{OUTPUT_DIR}/ComfyUI_{i}"

    print("Queueing:", file)
    cookie_name = os.environ["COOKIE_NAME"]
    cookie_value = os.environ["COOKIE_VALUE"]
    comfy_ui_url = os.environ["COMFY_UI_URL"]
    resp = requests.post(
        f"{comfy_ui_url}/prompt",
        json={"prompt": prompt},
        cookies={cookie_name: cookie_value},
    )

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e.response.text}")
