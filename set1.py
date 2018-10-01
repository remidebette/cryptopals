# encoding: utf8

import base64
import itertools
import operator
import os
from statistics import mean
from typing import List, Iterable
from itertools import cycle

from detect_english import is_english, score_english


def int_to_byte(i: int) -> bytes:
    """Helper to decode byte by byte an integer to a bytes"""
    return i.to_bytes((i.bit_length() + 7) // 8, 'big') or b''


def sum_digits(n: int, base=10) -> int:
    r = 0
    while n:
        r, n = r + n % base, n // base
    return r


def challenge1(message: bytes) -> bytes:
    return base64.b64encode(message)


def plain_key_xor(message: bytes, key: Iterable[bytes]):
    """Does bitwise XOR between a message and a key

    The length of the result will be the minimum between the lengths of the message and the key
    The key itself can be an iterable to support the repeating key pattern"""
    result = [
        # bitwise XOR operation works on integers in Python
        byte1 ^ byte2

        # iterating on bytes provides integers in python
        for byte1, byte2 in zip(message, key)
    ]

    return bytes(result)


def repeating_key_xor(message: bytes, key: bytes):
    """Apply the repeating key XOR pattern to the message"""

    # Itertool's *cycle* iterates over the key's items, which provides an integer iterator for the plain_key_xor
    # Itertool's *repeat* wouldn't have worked as smoothly
    return plain_key_xor(message, cycle(key))


def find_single_char_xor(byt: bytes) -> List[bytes]:
    matching_keys = []

    for i in range(0, 256):
        key = int_to_byte(i)
        deciphered_byt = repeating_key_xor(byt, key)
        if is_english(deciphered_byt):
            matching_keys.append(key)

    return matching_keys


def find_single_char_xor_score(byt: bytes, fail_threshold=0.0) -> bytes:
    scored_keys = []

    for i in range(0, 256):
        key = int_to_byte(i)
        deciphered_byt = repeating_key_xor(byt, key)
        score = score_english(deciphered_byt)
        scored_keys.append((key, score))

    final_key, final_score = max(scored_keys, key=operator.itemgetter(1))

    if final_score <= fail_threshold:
        return b''

    return final_key


def hamming_distance(key1: bytes, key2: bytes) -> int:
    # xor = plain_key_xor(key1, key2)
    # xor_int = int.from_bytes(xor, byteorder='big')
    #
    # return sum_digits(xor_int, base=2)
    return sum([bin(key1[i] ^ key2[i]).count('1') for i in range(len(key1))])


def edit_distance(message: bytes, key_size: int):
    first_blocks = [
        message[n * key_size:(n + 1) * key_size]
        for n in range(4)
    ]

    normalized_hammings = [hamming_distance(i, j) for i, j in itertools.combinations(first_blocks, 2)]
    return mean(normalized_hammings) / key_size


def challenge6(message: bytes):
    selected_size = min(range(2, 41), key=lambda k: edit_distance(message, k))

    substrings = [bytearray() for _ in range(selected_size)]
    for element, index in zip(message, cycle(range(selected_size))):
        substrings[index].append(element)

    key_list = [
        find_single_char_xor_score(substring, fail_threshold=3.0)
        for substring in substrings
    ]
    key = b"".join(key_list)

    deciphered_byt = repeating_key_xor(message, key)
    pass


if __name__ == '__main__':
    # Challenge 1
    challenge1_bytes = b"I'm killing your brain like a poisonous mushroom"
    print(f"Challenge 1 : {challenge1_bytes} gives base64 {challenge1(challenge1_bytes)}")

    # Challenge 2
    challenge2_1 = b'\x1c\x01\x11\x00\x1f\x01\x01\x00\x06\x1a\x02KSSP\t\x18\x1c'
    challenge2_2 = b"hit the bull's eye"

    print(f"Challenge 2 : {challenge2_1} XOR {challenge2_2} gives {plain_key_xor(challenge2_1, challenge2_2)}")

    # Challenge 3
    challenge3_bytes = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
    # my_keys = find_single_char_xor(challenge3_bytes)
    #
    # if my_keys:
    #     key = my_keys[0]
    #     deciphered_byt = repeating_key_xor(challenge3_bytes, key)
    #     print(f"Challenge 3 : {key}: {deciphered_byt.decode('ascii')}")

    key = find_single_char_xor_score(challenge3_bytes)
    deciphered_byt = repeating_key_xor(challenge3_bytes, key)
    print(f"Challenge 3 scored : {key}: {deciphered_byt.decode('ascii')}")

    # Challenge 4
    with open(os.path.join("data", "challenge4.txt"), encoding='ascii') as chall4:
        encoded_phrases = [bytes.fromhex(phrase) for phrase in chall4.read().splitlines()]

    acceptable_keys = [find_single_char_xor(phrase) for phrase in encoded_phrases]

    for index, phrase in enumerate(encoded_phrases):
        key = find_single_char_xor_score(phrase, fail_threshold=10.0)
        if key:
            deciphered_byt = repeating_key_xor(phrase, key)
            print(f"Challenge 4 : index {index}, key {key.decode('ascii')}, \n"
                  f"cipher {phrase}, decipher {deciphered_byt.decode('ascii')}")

    # Challenge 5
    with open(os.path.join("data", "challenge6.txt"), encoding='ascii') as chall4:
        text = chall4.read().replace('\n', '')
        data = base64.b64decode(text)

    challenge6(data)
    pass