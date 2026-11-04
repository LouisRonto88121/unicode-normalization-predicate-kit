# unicode-normalization-predicate-kit

Reports which Unicode normalization form (NFC, NFD, NFKC, NFKD) a given string is already in, so callers can skip redundant re-normalization.

```python
from unicode_normalization_predicate_kit import is_normalized, describe, normalization_forms

print(normalization_forms())   # ('NFC', 'NFD', 'NFKC', 'NFKD')
print(is_normalized("Á", "NFC"))   # True  (single precomposed code point U+00C1)
print(is_normalized("A\u0301", "NFC"))  # False (A + combining acute)
print(describe("hello"))      # ('NFC', 'NFD', 'NFKC', 'NFKD')
```

## Why this exists

If you store or forward text that is supposed to be normalized, calling `unicodedata.normalize` again is wasted work. This library tells you, in one call, which forms a string already satisfies, so you can skip the normalization pass entirely when it is a no-op.

The trade-off is straightforward: the check normalizes the string internally and compares, so it is not cheaper than normalizing. Use it when you normalise rarely but receive mostly-already-normal data and want to avoid the allocation churn of re-normalizing on the hot path.

## Edge case

A string can be in *several* forms at once (any ASCII string is in all four) or in *none* of them. `describe` returns a tuple of zero or more form names, in canonical NFC/NFD/NFKC/NFKD order; an empty result means the string is not in any form and does need normalizing.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

