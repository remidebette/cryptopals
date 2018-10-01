# encoding: utf8

import os
import string
from collections import Counter
from typing import Set


def load_dictionary() -> Set[bytes]:
    with open(os.path.join('data', 'dictionary.txt'), "rb") as dictionary_file:
        english_words = {word for word in dictionary_file.read().splitlines()}

    return english_words


ENGLISH_WORDS = load_dictionary()
acceptable_letters = (string.ascii_letters + string.whitespace).encode(encoding='ascii')
acceptable_set = {letter for letter in acceptable_letters}

# From http://www.data-compression.com/english.html
english_frequences = {
    b'a': 0.0651738,
    b'b': 0.0124248,
    b'c': 0.0217339,
    b'd': 0.0349835,
    b'e': 0.1041442,
    b'f': 0.0197881,
    b'g': 0.0158610,
    b'h': 0.0492888,
    b'i': 0.0558094,
    b'j': 0.0009033,
    b'k': 0.0050529,
    b'l': 0.0331490,
    b'm': 0.0202124,
    b'n': 0.0564513,
    b'o': 0.0596302,
    b'p': 0.0137645,
    b'q': 0.0008606,
    b'r': 0.0497563,
    b's': 0.0515760,
    b't': 0.0729357,
    b'u': 0.0225134,
    b'v': 0.0082903,
    b'w': 0.0171272,
    b'x': 0.0013692,
    b'y': 0.0145984,
    b'z': 0.0007836,
    b' ': 0.1918182
}
english_int_frequences = {
    int.from_bytes(key, byteorder='big'): value
    for key, value in english_frequences.items()
}


def score_english(s: bytes) -> float:
    score = 0
    for i in s.lower():
        if i in english_int_frequences:
            score += english_int_frequences[i]
    return score


def get_english_count(message: bytes) -> float:
    message = remove_non_letters(message)
    message = message.upper()
    possible_words = message.split()

    if not possible_words:
        return 0.0  # no words at all, so return 0.0

    matches = 0
    for word in possible_words:
        if word in ENGLISH_WORDS:
            matches += 1

    return float(matches) / len(possible_words)


def remove_non_letters(message: bytes) -> bytes:
    letters_only = [
        symbol
        for symbol in message
        if symbol in acceptable_set
    ]

    return bytes(letters_only)


def is_english(message: bytes, word_percentage=20, letter_percentage=85) -> bool:
    # By default, 20% of the words must exist in the dictionary file, and
    # 85% of all the characters in the message must be letters or spaces
    # (not punctuation or numbers).
    if not len(message):
        return False

    words_match = get_english_count(message) * 100 >= word_percentage
    num_letters = len(remove_non_letters(message))
    message_letters_percentage = float(num_letters) / len(message) * 100
    letters_match = message_letters_percentage >= letter_percentage

    return words_match and letters_match
