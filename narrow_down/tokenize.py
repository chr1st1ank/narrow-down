"""Set operations for string analysis."""
import collections
from typing import Dict, Set


def char_ngrams(s: str, n: int, pad_char: str = "$") -> Set[str]:
    """Get all character n-grams contained in the string s.

    Args:
        s: String to analyze
        n: The desired length of the n-grams. E.g. `3` to get 3-grams like `"abc"`, `"def"`
        pad_char: Padding character to use for the start and end of the string. Per default
            `"$"` is used, so that for example the string `ab` gives the following 2-grams:
            `"$a", "ab", "b$"`. Padding can be deactivated by setting pad_char to `""`.

    Returns:
        All different n-grams as a set of strings.
    """
    if not s:
        return set()
    padded = pad_char * (n - 1) + s + pad_char * (n - 1)
    return set(padded[i : i + n] for i in range(len(padded) - n + 1))


def count_char_ngrams(s: str, n: int, pad_char: str = "$") -> Dict[str, int]:
    """Count all character n-grams in s.

    Args:
        s: String to analyze
        n: The desired length of the n-grams. E.g. `3` to get 3-grams like `"abc"`, `"def"`
        pad_char: Padding character to use for the start and end of the string. Per default
            `"$"` is used, so that for example the string `ab` gives the following 2-grams:
            `"$a", "ab", "b$"`. Padding can be deactivated by setting pad_char to `""`.

    Returns:
        A dictionary which maps the found n-grams to the number of occurences.
    """
    if not s:
        return {}
    padded = pad_char * (n - 1) + s + pad_char * (n - 1)
    return collections.Counter(padded[i : i + n] for i in range(len(padded) - n + 1))
