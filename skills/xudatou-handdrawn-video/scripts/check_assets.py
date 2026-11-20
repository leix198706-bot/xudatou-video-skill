"""Check the local files available for a hand-drawn video character."""

import argparse
from pathlib import Path


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
AUDIO_SUFFIXES = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".opus"}
PREFIXES = {
    ".png": (b"\x89PNG\r\n\x1a\n",),
    ".jpg": (b"\xff\xd8\xff",),
    ".jpeg": (b"\xff\xd8\xff",),
    ".flac": (b"fLaC",),
    ".ogg": (b"OggS",),
    ".opus": (b"OggS",),
}


def matches_header(suffix, header):
    if suffix in PREFIXES:
        return header.startswith(PREFIXES[suffix])
    if suffix == ".webp":
        return header.startswith(b"RIFF") and header[8:12] == b"WEBP"
    if suffix == ".wav":
        return header.startswith((b"RIFF", b"RIFX", b"RF64")) and header[8:12] == b"WAVE"
    if suffix in {".m4a", ".mp4", ".mov"}:
        return len(header) >= 12 and header[4:8] in {b"ftyp", b"moov", b"mdat", b"wide", b"free"}
    if suffix == ".mp3":
        if header.startswith(b"ID3"):
            return len(header) >= 10
        return len(header) >= 4 and header[0] == 0xff and header[1] & 0xe0 == 0xe0
    if suffix == ".aac":
        return header.startswith(b"ADIF") or (
            len(header) >= 7 and header[0] == 0xff and header[1] & 0xf6 == 0xf0
        )
    return False


def is_recognized_media(path, suffixes):
    suffix = path.suffix.lower()
    if suffix not in suffixes:
        return False
    try:
        if not path.is_file():
            return False
        with path.open("rb") as file:
            return matches_header(suffix, file.read(16))
    except OSError:
        return False


def has_media(folder, suffixes, selected_file=None):
    candidates = (selected_file,) if selected_file is not None else folder.rglob("*")
    return any(is_recognized_media(path, suffixes) for path in candidates)


def main():
    parser = argparse.ArgumentParser(description="检查本地人物参考、配音样音与品牌素材。")
    parser.add_argument("persona", nargs="?", type=Path, default=Path("人物项目"), help="人物项目目录")
    parser.add_argument("--character", type=Path, help="已有角色基准图，可以使用绝对路径")
    parser.add_argument("--voice", type=Path, help="已有旁白参考音频，可以使用绝对路径")
    args = parser.parse_args()
    persona = args.persona.expanduser()
    character = persona / args.character.expanduser() if args.character else None
    voice = persona / args.voice.expanduser() if args.voice else None

    has_character = has_media(persona / "人物参考", IMAGE_SUFFIXES, character)
    has_voice = has_media(persona / "音色", AUDIO_SUFFIXES, voice)
    print("已找到人物参考。" if has_character else "缺少人物参考。请先制作一张角色基准图，或提供已有的角色参考图。")
    print("已找到音色。" if has_voice else "缺少音色。请先录制一段清晰的旁白样音，或选用已有授权的预设音色。")

    brand_folder = persona / "品牌素材"
    brand_assets = (
        ("水印", {".png"}),
        ("片尾", IMAGE_SUFFIXES | {".mp4", ".mov"}),
        ("封面参考", IMAGE_SUFFIXES),
    )
    missing = [label for label, suffixes in brand_assets if not has_media(brand_folder / label, suffixes)]
    if missing:
        print("按需补充 " + "、".join(missing) + "。")

    return 0 if has_character and has_voice else 1


if __name__ == "__main__":
    raise SystemExit(main())
