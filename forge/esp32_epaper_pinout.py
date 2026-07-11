"""Default ESP32 wiring information for an SPI e-paper display."""

from collections.abc import Mapping
import logging

logger = logging.getLogger(__name__)

ESP32_EPAPER_PINOUT: dict[str, str] = {
    "VCC": "3V3",
    "GND": "GND",
    "DIN": "GPIO23 (MOSI)",
    "CLK": "GPIO18 (SCK)",
    "CS": "GPIO5",
    "DC": "GPIO17",
    "RST": "GPIO16",
    "BUSY": "GPIO4",
}


def get_pinout() -> dict[str, str]:
    """Return a fresh copy of the default e-paper pinout."""
    return dict(ESP32_EPAPER_PINOUT)


def print_pinout(
    pinout: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Log the supplied or default pinout at INFO level."""
    selected_pinout = get_pinout() if pinout is None else dict(pinout)

    for signal, connection in selected_pinout.items():
        logger.info("%s: %s", signal, connection)

    return selected_pinout
