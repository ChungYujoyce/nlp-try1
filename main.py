from typing import Any, Iterable, List, Optional, Set, Tuple

from load import load_words
import math
import time
import vectors as v
from vectors import Vector
from word import Word

def most_similar(base_vector, words):
    start = time.time()
    # finds n words with smallest cosine similarity for a given word
    words_with_distance = [(v.cosine_similarity_normalized(base_vector, w.vector), w) for w in words]
    # want as large as 1
    sorted_by_dis = sorted(words_with_distance)
    print(f"Elapsed {time.time() - start} s")
    return sorted_by_dis

def print_most_similar(words, text):
    base_word = find_word(text, words)
    if not base_word:
        print(f"Uknown word: {text}")
        return
    print(f"Words related to {base_word.text}:")
    sorted_by_dis = [word.text for (dist, word) in most_similar(base_word.vector, words)
    if word.text.lower() != base_word.text.lower()]

    print(', '.join(sorted_by_dis[:10]))

def read_word():
    return input("Type a word...")

def find_word(text, words):
    try:
        return next(w for w in words if text == w.text)
    except StopIteration:
        return None

def closest_analogy(left2, left1, right2, words):
    word_left1 = find_word(left1, words)
    word_left2 = find_word(left2, words)
    word_right2 = find_word(right2, words)
    if (not word_left1) or (not word_left2) or (not word_right2):
        return []

    vector = v.add(v.sub(word_left1.vector, word_left2.vector), word_right2.vector)
    closest = most_similar(vector, words)[:10]

    def is_redundant(word):
        """
        Sometimes the two left vectors are so close the answer is e.g.
        "shirt-clothing is like phone-phones". Skip 'phones' and get the next
        suggestion, which might be more interesting.
        """
        word_lower = word.lower()
        return (
            left1.lower() in word_lower or
            left2.lower() in word_lower or
            right2.lower() in word_lower)

    closest_filtered = [(dist, w) for (dist, w) in closest if not is_redundant(w.text)]
    return closest_filtered

def print_analogy(left2, left1, right2, words):
    analogy = closest_analogy(left2, left1, right2, words)
    if (len(analogy) == 0):
        print(f"{left2}-{left1} is like {right2}-?")
    else:
        (dist, w) = analogy[0]
        print(f"{left2}-{left1} is like {right2}-{w.text}")

words = load_words('words-short.vec')

print_most_similar(words, words[190].text)
print_most_similar(words, words[230].text)
print_most_similar(words, words[330].text)
print_most_similar(words, words[430].text)

print("-----------------------------------")
print_analogy('quick', 'quickest' , 'far', words)
print_analogy('sushi', 'rice', 'pizza', words)
print_analogy('Paris', 'France', 'Rome', words)
print_analogy('dog', 'mammal', 'eagle', words)
print_analogy('German', 'BMW' , 'American', words)
print_analogy('German', 'Opel', 'American', words)

# analogies
while False:
    left2 = find_word(read_word(), words)
    if not left2:
        print("Sorry, I don't know that word.")
        continue
    left1 = find_word(read_word(), words)
    if not left1:
        print("Sorry, I don't know that word.")
        continue
    right2 = find_word(read_word(), words)
    if not right2:
        print("Sorry, I don't know that word.")
        continue
    print_analogy(left2, left1, right2, words)

# Related words (interactive)
while False:
    text = read_word()
    w = find_word(text, words)
    if not w:
        print("Sorry, I don't know that word.")
    else:
        print_most_similar(w)