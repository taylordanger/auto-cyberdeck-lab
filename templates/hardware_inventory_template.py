"""Generate a hardware inventory CSV from the bundled template."""

from pathlib import Path
import shutil

TEMPLATE_PATH = Path(__file__).with_name("hardware_inventory_template.csv")
DEFAULT_OUTPUT_PATH = Path("hardware_inventory_template.csv")


def get_template_path() -> Path:
    """Return the path to the bundled hardware inventory template."""
    if not TEMPLATE_PATH.is_file():
        raise FileNotFoundError(
            f"Hardware inventory template not found: {TEMPLATE_PATH}"
        )

    return TEMPLATE_PATH


def generate_hardware_inventory_template(
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> Path:
    """Copy the bundled hardware inventory CSV to an output location.

    Args:
        output_path: Destination for the generated CSV file.

    Returns:
        The destination path.

    Raises:
        FileNotFoundError: If the bundled CSV template is missing.
        IsADirectoryError: If the destination is an existing directory.
    """
    source = get_template_path()
    destination = Path(output_path)

    if destination.exists() and destination.is_dir():
        raise IsADirectoryError(
            f"Output path is a directory: {destination}"
        )

    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.resolve() == source.resolve():
        return destination

    temporary_path = destination.with_name(
        f".{destination.name}.tmp"
    )

    try:
        shutil.copyfile(source, temporary_path)
        temporary_path.replace(destination)
    finally:
        temporary_path.unlink(missing_ok=True)

    return destination


# Small compatibility alias for callers using a generic generator name.
generate_template = generate_hardware_inventory_template


def generate() -> str:
    """Return the bundled hardware inventory CSV template as text."""
    return get_template_path().read_text(encoding="utf-8")
