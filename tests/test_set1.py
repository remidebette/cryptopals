import pytest

from set1 import challenge1, challenge2


def test_challenge1():
    given = bytes.fromhex("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d")
    expected = b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    assert expected == challenge1(given)


@pytest.mark.parametrize("in1, in2, expected", [
    ("1c0111001f010100061a024b53535009181c", "686974207468652062756c6c277320657965", "746865206b696420646f6e277420706c6179"),
    ("1c011100", "686974207468652062756c6c277320657965", "74686520"),
    ("1c0111001f010100061a024b53535009181c", "68697420", "74686520"),
    ("", "68697420", ""),
    ("1c011100", "", ""),
    ("", "", "")
])
def test_challenge2(in1, in2, expected):
    by1 = bytes.fromhex(in1)
    by2 = bytes.fromhex(in2)
    expected = bytes.fromhex(expected)

    assert expected == challenge2(by1, by2)


# def test_challenge3():
#     given = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")