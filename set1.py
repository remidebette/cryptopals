import base64


def challenge1(byt: bytes):
    return base64.b64encode(byt)


def challenge2(by1: bytes, by2: bytes):
    min_len = min(len(by1), len(by2))
    int1 = int.from_bytes(by1[:min_len], byteorder='big')
    int2 = int.from_bytes(by2[:min_len], byteorder='big')
    result = int1 ^ int2

    return result.to_bytes((result.bit_length() + 7) // 8, 'big') or b''