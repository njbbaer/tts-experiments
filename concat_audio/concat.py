from pydub import AudioSegment

INTERVAL = 500
TEMPO = 1.0

with open("concat_audio/concat.txt") as f:
    files = [line.strip() for line in f]

silence = AudioSegment.silent(duration=INTERVAL)

combined = AudioSegment.empty()
for i, file in enumerate(files):
    seg = AudioSegment.from_file(file)
    combined += seg
    if i < len(files) - 1:
        combined += silence

names = [file.split("/")[-1].split(".")[0] for file in files]
output_file = f"concat_audio/output/{"_".join(names) + ".wav"}"

combined.export(output_file, format="wav", parameters=["-filter:a", f"atempo={TEMPO}"])
