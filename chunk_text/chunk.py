import re, shutil
from pathlib import Path


def main():
    source_path = Path("./chunk_text/text.txt")
    output_path = Path("./chunk_text/output")
    min_chars = 1000

    text = source_path.read_text(encoding="utf-8")
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks, buf, size = [], [], 0
    for p in paras:
        if buf:
            size += 2
        buf.append(p)
        size += len(p)
        if size >= min_chars:
            chunks.append("\n\n".join(buf))
            buf, size = [], 0
    if buf:
        chunks.append("\n\n".join(buf))

    shutil.rmtree(output_path, ignore_errors=True)
    output_path.mkdir(parents=True, exist_ok=True)

    w = max(3, len(str(len(chunks))))

    for i, c in enumerate(chunks):
        (output_path / f"{i:0{w}d}.txt").write_text(c, encoding="utf-8")


if __name__ == "__main__":
    main()
