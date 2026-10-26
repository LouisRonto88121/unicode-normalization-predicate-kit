"""Core predicate logic for Unicode normalization forms.

We use the standard-library ``unicodedata`` module for the actual
normalization work and build predicates on top of it.  The fundamental
trick is simple: a string is already in form X iff normalizing it to X
is a no-op.

Design choice: every public function accepts ``str`` only.  Passing
``bytes`` raises ``TypeError`` deliberately — a silent coercion would
hide mistakes and the caller's intent is never unambiguous.
"""

from __future__ import annotations

import unicodedata

# A frozen, ordered tuple of the four normalization forms Python's
# standard library knows about.  Tuple (rather than list) so callers
# cannot mutate the canonical order via the exported reference.
FORMS = ("NFC", "NFD", "NFKC", "NFKD")


def normalization_forms() -> tuple[str, ...]:
    """Return the normalization forms this library can test.

    The order is NFC, NFD, NFKC, NFKD — the order used by UAX #15.
    """
    return FORMS


def _ensure_str(s: object) -> str:
    if not isinstance(s, str):
        raise TypeError(
            "expected str, got " + type(s).__name__,
        )
    return s


def is_normalized(s, form: str) -> bool:
    """Return True if *s* is already in normalization *form*.

    ``form`` must be one of NFC, NFD, NFKC, NFKD (case-insensitive,
    matching ``unicodedata.normalize``).  Any other value raises
    ``ValueError``, surfaced directly from ``unicodedata``.
    """
    text = _ensure_str(s)
    return unicodedata.normalize(form, text) == text


def describe(s) -> tuple[str, ...]:
    """Return the forms *s* is already normalized to.

    Always returns a tuple of zero or more of NFC, NFD, NFKC, NFKD
    in canonical order.  An empty tuple means the string is in none of
    the four forms (e.g. a string with mixed precomposed and decomposed
    code points for the same abstract character).
    """
    text = _ensure_str(s)
    return tuple(form for form in FORMS if unicodedata.normalize(form, text) == text)
