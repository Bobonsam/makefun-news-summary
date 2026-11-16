"""Copy the stored 11 November 2026 news summary to entry.txt.

The summary lives in summary.txt next to this file. This program reads
it as raw bytes, validates it, and writes the exact same bytes to
entry.txt inside the output directory. Standard library only; no
network, randomness or time dependence, so repeated runs agree.
"""

import os
import sys
from pathlib import Path

LOWEST_OK = 1
HIGHEST_OK = 2000
FALLBACK_DIR = "/output"
ENTRY_NAME = "entry.txt"
SOURCE_NAME = "summary.txt"


class BadSummary(Exception):
    """Raised when summary.txt fails validation."""


def source_file() -> Path:
    return Path(__file__).resolve().parent / SOURCE_NAME


def read_payload() -> bytes:
    return source_file().read_bytes()


def validate_payload(payload: bytes) -> None:
    try:
        decoded = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise BadSummary("summary.txt is not valid UTF-8") from exc
    count = len(decoded)
    if count < LOWEST_OK or count > HIGHEST_OK:
        raise BadSummary(
            f"summary is {count} characters, expected {LOWEST_OK}-{HIGHEST_OK}"
        )
    if decoded.strip() == "":
        raise BadSummary("summary is only whitespace")


def destination_file() -> Path:
    name = os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_DIR
    folder = Path(name)
    folder.mkdir(parents=True, exist_ok=True)
    return folder / ENTRY_NAME


def main() -> int:
    try:
        payload = read_payload()
        validate_payload(payload)
        destination_file().write_bytes(payload)
    except BadSummary as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
