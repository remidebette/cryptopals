import os
import string
from typing import Set


def load_dictionary() -> Set[bytes]:
    with open(os.path.join('data', 'dictionary.txt'), "rb") as dictionary_file:
        english_words = {word for word in dictionary_file.read().splitlines()}

    return english_words


ENGLISH_WORDS = load_dictionary()
acceptable_letters = (string.ascii_letters + string.whitespace).encode(encoding='ascii')
acceptable_set = {letter for letter in acceptable_letters}


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


# coding: utf8

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
