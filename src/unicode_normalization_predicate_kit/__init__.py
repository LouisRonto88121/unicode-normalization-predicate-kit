"""unicode-normalization-predicate-kit

Report which Unicode normalization form a given string is already in.
"""

from .core import (
    normalization_forms,
    is_normalized,
    describe,
)

__all__ = [
    "normalization_forms",
    "is_normalized",
    "describe",
]
