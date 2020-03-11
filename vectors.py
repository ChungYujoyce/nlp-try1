from typing import List

import math

Vector = List[float]

# define some math for measuring similarity
def l2_len(v):
    return math.sqrt(sum([x*x for x in v]))

def dot(v1, v2):
    assert len(v1) == len(v2)
    return sum([x*y for (x,y) in zip(v1, v2)])

def add(v1, v2):
    assert len(v1) == len(v2)
    return [x + y for (x,y) in zip(v1, v2)]

def sub(v1, v2):
    assert len(v1) == len(v2)
    return [x - y for (x,y) in zip(v1, v2)]

def normalize(v):
    l = l2_len(v)
    return [x / l for x in v]

"""
    Returns the cosine of the angle between the two vectors.
    Each of the vectors must have length (L2-norm) equal to 1.
    Results range from -1 (very different) to 1 (very similar).
"""
def cosine_similarity_normalized(v1, v2):
    return dot(v1, v2)
