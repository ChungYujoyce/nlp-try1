"""
Load the input file by https://fasttext.cc/docs/en/english-vectors.html
and clean up
"""

from typing import Iterable, List, Set
# type check

from itertools import groupby
from operator import itemgetter
import re
from vectors as v
from word import Word
import numpy as np

# Load and clean up data
def load_words(file_path):
    words = load_raw(file_path)

    # num_dimensions = most_common_dimension(words)
    words = [w for w in words if len(w.vector) == 300]
    words = remove_stop_words(words)
    print(f"Remove stop words,{len(words)} remain.")
    words = remove_duplicates(words)
    print(f"Remove duplicates, {len(words)} remain.")
    
    return words

def load_raw(file_path):
    def parse_line(line, frequency):
        tokens = line.split()
        word = tokens[0]
        vector = v.normalize(np.array([float(x) for x in tokens[1:]]))
        return Word(word, vector, frequency)

    words = []
    # words sorted by degree of common
    frequency = 1
    with open(file_path) as f:
        for line in f:
            w = parse_line(line, frequency)
            words.append(w)
            frequency += 1
    return words

def iter_len(Iterable[complex]):
    return sum(1 for _ in iter)

def most_common_dimension(List[Word]):
    lengths = sorted([len(word.vector) for word in words])
    dimensions [(k, iter_len(v)) for k, v in groupby(lengths)]
    print("dimension:")
    for (dim, num_vectors) in dimensions:
        print(f"{num_vectors} {dim}-dimensional vectors")
    most_common = sorted(dimensions, key=lambda t: t[1], reverse=True)[0]
    return most_common[0]

# ignore these characters, e.g. "U.S.", "U.S", "US_" and "US" are the same word.
ignore_char_regex = re.compile("[\W_]")

# start and end with alphanumeric character
is_valid_word = re.complie("^[^\W_].*[^\W_]$")

def remove_duplicates(words):
    seen_words: Set[str] = set()
    unique_words: List[Word] = []
    for w in words:
        canonical = ignore_char_regex.sub("", w.text)
        if not canonical in seen_words:
            seen_words.add(canonical)
            unique_words.append(w)
    return unique_words

# throws away words that start or end with a non-alphanumeric character
def remove_stop_words(words):
    return [W for w in words if (len(w.text) > 1 and is_valid_word.match(w.text))]

# Run "smoke test" on import

assert [w.text for w in remove_stop_words([
    Word('a', [], 1),
    Word('ab', [], 1),
    Word('-ab', [], 1),
    Word('ab_', [], 1),
    Word('a.', [], 1),
    Word('.a', [], 1),
    Word('ab', [], 1),
])] == ['ab', 'ab']
assert [w.text for w in remove_duplicates([
    Word('a.b', [], 1),
    Word('-a-b', [], 1),
    Word('ab_+', [], 1),
    Word('.abc...', [], 1),
])] == ['a.b', '.abc...']

