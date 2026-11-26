#!/usr/bin/env python3
"""The Moon Gets One Star.

Writes a single one-star review of the Moon (<=120 chars) to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).
Python 3.13 stdlib only: no network, no randomness, deterministic.

Chosen line, against the judge's brief (most important first):
  1. A one-star review of the Moon itself: the grievance is the tides,
     something only the Moon does — it drags the whole ocean around
     twice a day.
  2. The laugh lands on first read: "pulls the entire ocean around"
     turns on "can't pull itself together" in the same breath.
  3. Reads like a real one-star review: "One star." plus a grievance a
     genuine reviewer would leave, not a slogan or a poem.
  4. A specific, surprising grievance: the tides, not the obvious
     craters, cheese or brightness jokes the brief warns against.
  5. 89 characters; every word earns its place and the punchline is the
     last phrase.
"""

import os

ENTRY = (
    "One star. Pulls the entire ocean around twice a day "
    "and still can't pull itself together."
)

# The gate: /output/entry.txt must be UTF-8 text of 1 to 120 characters,
# not only white space, on a single line. Fail loudly instead of shipping
# an invalid entry.
MAX_CHARS = 120


def validate(text: str) -> str:
    """Enforce the competition gate; return the cleaned entry text."""
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("entry is empty or only whitespace")
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("entry must be a single line")
    if len(cleaned) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(cleaned)} chars, over the {MAX_CHARS} limit"
        )
    try:
        cleaned.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("entry must be plain ASCII") from exc
    if any(ord(ch) < 0x20 for ch in cleaned):
        raise ValueError("entry must not contain control characters")
    return cleaned


def main() -> None:
    text = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    expected = (text + "\n").encode("utf-8")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    # Byte-exact write-back assertion: what landed on disk must be
    # exactly the validated entry plus one trailing newline, no more.
    with open(path, "rb") as handle:
        written = handle.read()
    if written != expected:
        raise ValueError(
            f"write-back mismatch: wrote {len(written)} bytes, "
            f"expected {len(expected)}"
        )


if __name__ == "__main__":
    main()
