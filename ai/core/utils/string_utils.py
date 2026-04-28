import warnings
from typing import Any, Optional


def str_to_bool(val_str: str) -> bool:
    normalized = val_str.strip().lower()
    if normalized == "true":
        return True
    elif normalized == "false":
        return False
    else:
        warnings.warn(
            f"Unsupported string value: '{val_str}'. "
            "Supports only 'True', 'true', 'False', or 'false'. Returning False."
        )
        return False


def is_empty_string(string: str | None) -> bool:
    """Return True if the string is None or contains only whitespace."""
    return string is None or not string.strip()


def clean_optional_string(value: Optional[Any]) -> Optional[str]:
    """Return a trimmed string if value is a valid non-empty string, else
    None."""
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return None
