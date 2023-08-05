# from struct import pack
from .utils import int2bytes, bytes2int


def decrypt(crypto, n, d):
    return int2bytes(pow(bytes2int(crypto), d, n))


def encrypt(message, n, e):
    i = bytes2int(message)
    assert i <= n
    return int2bytes(pow(i, e, n))


def vencrypt(n, e, src, out):
    from random import SystemRandom
    from .varint import encode, encode_stream

    # from sys import stderr

    random = SystemRandom()
    bits_max = n.bit_length()
    q, r = divmod(bits_max - 1, 8)
    bytes_max = q if q > 0 else q + 1
    getrandbits = random.getrandbits

    def mkprefix(x):
        return bytes(encode(getrandbits(random.randrange(32, 48)))) + bytes(encode(x))

    i = 0
    prefix = mkprefix(i)
    block = src.read(bytes_max - len(prefix))
    while block:
        cypher = encrypt(prefix + block, n, e)
        # print('E', i, len(cypher), file=stderr)
        encode_stream(out, len(cypher))
        out.write(cypher)
        # print('blob', blob)
        i += 1
        prefix = mkprefix(i)
        block = src.read(bytes_max - len(prefix))


def vdecrypt(n, d, src, out, i=0):
    from .varint import decode_stream
    from io import BytesIO

    s = decode_stream(src)
    while s > 0:
        cypher = src.read(s)
        blob = decrypt(cypher, n, d)
        # print('D', i, s, len(blob))
        b = BytesIO(blob)
        salt = decode_stream(b)
        index = decode_stream(b)
        block = b.read()
        # print(n, index, salt, blob)
        assert index == i
        assert salt != 0
        out.write(block)
        i += 1
        s = decode_stream(src)
