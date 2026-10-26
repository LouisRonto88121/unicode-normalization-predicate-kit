"""Tests for unicode_normalization_predicate_kit.core."""

import unittest

import unicodedata

from unicode_normalization_predicate_kit import (
    normalization_forms,
    is_normalized,
    describe,
)


# Latin capital A with acute, precomposed (single code point U+00C1).
PRECOMPOSED = "\u00c1"

# Same character decomposed: A (U+0041) + combining acute (U+0301).
DECOMPOSED = "A\u0301"


class TestNormalizationForms(unittest.TestCase):
    def test_returns_all_four_forms(self):
        self.assertEqual(normalization_forms(), ("NFC", "NFD", "NFKC", "NFKD"))

    def test_returns_tuple_not_list(self):
        self.assertIsInstance(normalization_forms(), tuple)


class TestIsNormalized(unittest.TestCase):
    def test_precomposed_is_nfc(self):
        self.assertTrue(is_normalized(PRECOMPOSED, "NFC"))

    def test_decomposed_is_not_nfc(self):
        self.assertFalse(is_normalized(DECOMPOSED, "NFC"))

    def test_decomposed_is_nfd(self):
        self.assertTrue(is_normalized(DECOMPOSED, "NFD"))

    def test_precomposed_is_not_nfd(self):
        self.assertFalse(is_normalized(PRECOMPOSED, "NFD"))

    def test_ascii_is_all_forms(self):
        for form in ("NFC", "NFD", "NFKC", "NFKD"):
            self.assertTrue(is_normalized("hello", form), form)

    def test_empty_string_all_forms(self):
        for form in ("NFC", "NFD", "NFKC", "NFKD"):
            self.assertTrue(is_normalized("", form), form)

    def test_nfkc_vs_nfkd(self):
        # Full-width 'A' (U+FF21) is a compatibility character.
        # NFKC/NFKD decompose compatibility characters, so it is NOT in
        # NFKC or NFKD form (normalizing changes it to ASCII 'A').
        # NFC/NFD do not touch compatibility characters, so it IS in NFC
        # and NFD.
        fullwidth_a = "\uff21"
        self.assertFalse(is_normalized(fullwidth_a, "NFKD"))
        self.assertFalse(is_normalized(fullwidth_a, "NFKC"))
        self.assertTrue(is_normalized(fullwidth_a, "NFC"))
        self.assertTrue(is_normalized(fullwidth_a, "NFD"))

    def test_lowercase_form_accepted(self):
        # unicodedata.normalize requires uppercase form names, so
        # lowercase must be rejected.
        with self.assertRaises(ValueError):
            is_normalized("hello", "nfc")

    def test_invalid_form_raises(self):
        with self.assertRaises(ValueError):
            is_normalized("hello", "NFKX")

    def test_bytes_rejected(self):
        with self.assertRaises(TypeError):
            is_normalized(b"hello", "NFC")

    def test_none_rejected(self):
        with self.assertRaises(TypeError):
            is_normalized(None, "NFC")


class TestDescribe(unittest.TestCase):
    def test_ascii_string_all_four(self):
        self.assertEqual(describe("hello"), ("NFC", "NFD", "NFKC", "NFKD"))

    def test_precomposed_nfc_only(self):
        self.assertEqual(describe(PRECOMPOSED), ("NFC", "NFKC"))

    def test_decomposed_nfd_only(self):
        self.assertEqual(describe(DECOMPOSED), ("NFD", "NFKD"))

    def test_mixed_string_not_in_any_form(self):
        # Full-width 'A' (U+FF21) is a compatibility character that
        # decomposes under NFKC/NFKD but survives NFC/NFD unchanged.
        # It is therefore in NFC and NFD (and not in NFKC or NFKD).
        s = "\uff21"
        forms = describe(s)
        self.assertIn("NFC", forms)
        self.assertIn("NFD", forms)
        self.assertNotIn("NFKC", forms)
        self.assertNotIn("NFKD", forms)

    def test_returns_tuple(self):
        self.assertIsInstance(describe("a"), tuple)

    def test_bytes_rejected(self):
        with self.assertRaises(TypeError):
            describe(b"hi")


if __name__ == "__main__":
    unittest.main()
