# coding: utf8

import base64
import os
from typing import List, Iterable
from itertools import cycle

from detect_english import is_english


def int_to_byte(i: int) -> bytes:
    """Helper to decode byte by byte an integer to a bytes"""
    return i.to_bytes((i.bit_length() + 7) // 8, 'big') or b''


def challenge1(message: bytes) -> bytes:
    return base64.b64encode(message)


def finished_key_xor(message: bytes, key: Iterable[bytes]):
    """Does bytewise XOR between a message and a key

    The length of the result will be the minimum between the lengths of the message and the key
    The key itself can be an iterable to support the repeating key pattern"""
    result = [
        # bytewise XOR operation works on integers in Python
        byte1 ^ byte2

        # iterating on bytes gives integers in python
        for byte1, byte2 in zip(message, key)
    ]

    return bytes(result)


def repeating_key_xor(message: bytes, key: bytes):
    """Apply the repeating key XOR pattern to the message"""

    # Itertool's *cycle* iterates over the key's items, which provides an integer iterator for the finished_key_xor
    # Itertool's *repeat* wouldn't have worked as smoothly
    return finished_key_xor(message, cycle(key))


def challenge3(byt: bytes) -> List[bytes]:
    matching_keys = []

    for i in range(1, 127):
        key = int_to_byte(i)
        deciphered_byt = repeating_key_xor(byt, key)
        if is_english(deciphered_byt):
            matching_keys.append(key)

    return matching_keys


if __name__ == '__main__':
    # Challenge 1
    challenge1_bytes = b"I'm killing your brain like a poisonous mushroom"
    print(f"Challenge 1 : {challenge1_bytes} gives base64 {challenge1(challenge1_bytes)}")

    # Challenge 2
    challenge2_1 = b'\x1c\x01\x11\x00\x1f\x01\x01\x00\x06\x1a\x02KSSP\t\x18\x1c'
    challenge2_2 = b"hit the bull's eye"

    print(f"Challenge 2 : {challenge2_1} XOR {challenge2_2} gives {finished_key_xor(challenge2_1, challenge2_2)}")

    # Challenge 3
    challenge3_bytes = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
    my_keys = challenge3(challenge3_bytes)

    if my_keys:
        key = my_keys[0]
        deciphered_byt = repeating_key_xor(challenge3_bytes, key)
        print(f"Challenge 3 : {key}: {deciphered_byt.decode('ascii')}")

    # Challenge 4
    with open(os.path.join("data", "challenge4.txt"), encoding='ascii') as chall4:
        encoded_phrases = [bytes.fromhex(phrase) for phrase in chall4.read().splitlines()]

    acceptable_keys = [challenge3(phrase) for phrase in encoded_phrases]

    for index, phrase in enumerate(encoded_phrases):
        my_keys = challenge3(phrase)
        if my_keys:
            key = my_keys[0]
            deciphered_byt = repeating_key_xor(phrase, key)
            print(f"Challenge 4 : index {index}, key {key}, \n"
                  f"cipher {phrase}, decipher {deciphered_byt.decode('ascii')}")
