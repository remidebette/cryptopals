import base64


def challenge1(byt: bytes):
    return base64.b64encode(byt)


def challenge2(by1: bytes, by2: bytes):
    min_len = min(len(by1), len(by2))
    int1 = int.from_bytes(by1[:min_len], byteorder='big')
    int2 = int.from_bytes(by2[:min_len], byteorder='big')

    # bytewise XOR operation works on integers in Python
    result = int1 ^ int2

    return result.to_bytes((result.bit_length() + 7) // 8, 'big') or b''


if __name__ == '__main__':
    challenge1_bytes = b"I'm killing your brain like a poisonous mushroom"
    print(f"Challenge 1 : {challenge1_bytes} gives base64 {challenge1(challenge1_bytes)}")

    challenge2_1 = b'\x1c\x01\x11\x00\x1f\x01\x01\x00\x06\x1a\x02KSSP\t\x18\x1c'
    challenge2_2 = b"hit the bull's eye"

    print(f"Challenge 2 : {challenge2_1} XOR {challenge2_2} gives {challenge2(challenge2_1, challenge2_2)}")