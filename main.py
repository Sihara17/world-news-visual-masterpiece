"""Write the fixed, offline editorial image required by make.fun."""

from pathlib import Path
import os
import shutil
import zlib


LIMIT_BYTES = 1_048_576
LIMIT_EDGE = 1_024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def dimensions(data: bytes) -> tuple[int, int]:
    """Read dimensions from a complete PNG or JPEG using only the stdlib."""
    if data.startswith(PNG_SIGNATURE):
        offset = len(PNG_SIGNATURE)
        image_size = None
        while offset + 12 <= len(data):
            length = int.from_bytes(data[offset:offset + 4], "big")
            end = offset + 12 + length
            if end > len(data):
                break
            kind = data[offset + 4:offset + 8]
            content = data[offset + 8:offset + 8 + length]
            checksum = int.from_bytes(data[offset + 8 + length:end], "big")
            if zlib.crc32(kind + content) & 0xFFFFFFFF != checksum:
                raise ValueError("entry.png contains a PNG chunk with a bad checksum")
            if kind == b"IHDR" and length == 13:
                image_size = (int.from_bytes(content[:4], "big"), int.from_bytes(content[4:8], "big"))
            if kind == b"IEND":
                if length != 0 or end != len(data) or image_size is None:
                    break
                return image_size
            offset = end
        raise ValueError("entry.png is not a complete PNG")

    if not data.startswith(b"\xff\xd8") or not data.endswith(b"\xff\xd9"):
        raise ValueError("entry.png must be a complete PNG or JPEG")

    start_of_frame = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    offset = 2
    while offset < len(data) - 2:
        if data[offset] != 0xFF:
            offset += 1
            continue
        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        if offset >= len(data):
            break
        marker = data[offset]
        offset += 1
        if marker in {0xD8, 0xD9} or 0xD0 <= marker <= 0xD7 or marker == 0x01:
            continue
        if offset + 2 > len(data):
            break
        length = int.from_bytes(data[offset:offset + 2], "big")
        if length < 2 or offset + length > len(data):
            break
        if marker in start_of_frame and length >= 7:
            height = int.from_bytes(data[offset + 3:offset + 5], "big")
            width = int.from_bytes(data[offset + 5:offset + 7], "big")
            return width, height
        offset += length
    raise ValueError("entry.png has no valid JPEG frame")


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    image = source.read_bytes()
    if len(image) > LIMIT_BYTES:
        raise ValueError("entry.png exceeds 1 MiB")
    width, height = dimensions(image)
    if width > LIMIT_EDGE or height > LIMIT_EDGE:
        raise ValueError("entry.png exceeds 1024 by 1024 pixels")

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output_dir / "entry.png")


if __name__ == "__main__":
    main()
