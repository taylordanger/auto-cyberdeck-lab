"""Generate validated bitmaps for a 60-by-9 LED display."""

from collections.abc import Sequence
from pathlib import Path
import struct
import zlib

LED_WIDTH = 60
LED_HEIGHT = 9

Bitmap = list[list[int]]
BitmapInput = Sequence[Sequence[int | bool]]


def _png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    """Build one PNG data chunk."""
    checksum = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    return (
        struct.pack(">I", len(data))
        + chunk_type
        + data
        + struct.pack(">I", checksum)
    )


def _write_png(bitmap: Bitmap, output_path: Path) -> None:
    """Write the bitmap as an 8-bit grayscale PNG."""
    raw_rows = b"".join(
        b"\x00" + bytes(255 if pixel else 0 for pixel in row)
        for row in bitmap
    )

    header = struct.pack(
        ">IIBBBBB",
        LED_WIDTH,
        LED_HEIGHT,
        8,  # bit depth
        0,  # grayscale
        0,  # compression method
        0,  # filter method
        0,  # no interlacing
    )

    png_data = (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", header)
        + _png_chunk(b"IDAT", zlib.compress(raw_rows))
        + _png_chunk(b"IEND", b"")
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = output_path.with_name(output_path.name + ".tmp")
    temporary_path.write_bytes(png_data)
    temporary_path.replace(output_path)


def _normalize_bitmap(bitmap: BitmapInput | None) -> Bitmap:
    """Validate and copy a 60-by-9 binary bitmap."""
    if bitmap is None:
        return [[0] * LED_WIDTH for _ in range(LED_HEIGHT)]

    if isinstance(bitmap, (str, bytes, bytearray)) or not isinstance(
        bitmap, Sequence
    ):
        raise TypeError("bitmap must be a sequence of rows")

    if len(bitmap) != LED_HEIGHT:
        raise ValueError(
            f"bitmap must contain exactly {LED_HEIGHT} rows; "
            f"received {len(bitmap)}"
        )

    normalized: Bitmap = []

    for row_index, source_row in enumerate(bitmap):
        if isinstance(source_row, (str, bytes, bytearray)) or not isinstance(
            source_row, Sequence
        ):
            raise TypeError(f"row {row_index} must be a sequence of pixels")

        if len(source_row) != LED_WIDTH:
            raise ValueError(
                f"row {row_index} must contain exactly {LED_WIDTH} pixels; "
                f"received {len(source_row)}"
            )

        row: list[int] = []

        for column_index, pixel in enumerate(source_row):
            if isinstance(pixel, bool):
                row.append(int(pixel))
            elif isinstance(pixel, int) and pixel in (0, 1):
                row.append(pixel)
            else:
                raise ValueError(
                    f"pixel at row {row_index}, column {column_index} "
                    f"must be 0 or 1; received {pixel!r}"
                )

        normalized.append(row)

    return normalized


def generate_led_bitmap(
    bitmap: BitmapInput | None = None,
    output_path: str | Path | None = "led_bitmap.png",
) -> Bitmap:
    """Validate, return, and optionally save a 60-by-9 LED bitmap.

    Calling this function without arguments creates a blank bitmap and writes
    it to ``led_bitmap.png``.

    Args:
        bitmap: Nine rows containing sixty binary pixels each. When omitted,
            a blank bitmap is generated.
        output_path: PNG destination. Pass ``None`` to skip writing a file.

    Returns:
        A fresh nested list containing integer values of 0 or 1.

    Raises:
        TypeError: If the bitmap structure uses unsupported types.
        ValueError: If its dimensions or pixel values are invalid.
    """
    normalized = _normalize_bitmap(bitmap)

    if output_path is not None:
        _write_png(normalized, Path(output_path))

    return normalized
