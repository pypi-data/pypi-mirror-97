"""
Copied from Python-RSA
"""
from binascii import hexlify
from struct import pack
from os import urandom


def bytes2int(raw_bytes):
    return int(hexlify(raw_bytes), 16)


def byte_size(n):
    if n == 0:
        return 1
    q, r = divmod(n.bit_length(), 8)
    return (q + 1) if r else q


def int2bytes(n):
    if n < 0:
        raise ValueError("Negative numbers cannot be used: %i" % n)
    elif n == 0:
        return b"\x00"
    a = []
    while n > 0:
        a.append(pack("B", n & 0xFF))
        n >>= 8
    a.reverse()
    return b"".join(a)


#########


def read_random_bits(nbits):
    """Reads 'nbits' random bits.

    If nbits isn't a whole number of bytes, an extra byte will be appended with
    only the lower bits set.
    """

    nbytes, rbits = divmod(nbits, 8)

    # Get the random bytes
    randomdata = urandom(nbytes)

    # Add the remaining random bits
    if rbits > 0:
        randomvalue = ord(urandom(1))
        randomvalue >>= 8 - rbits
        randomdata = pack("B", randomvalue) + randomdata

    return randomdata


def read_random_int(nbits):
    """Reads a random integer of approximately nbits bits."""

    randomdata = read_random_bits(nbits)
    value = bytes2int(randomdata)

    # Ensure that the number is large enough to just fill out the required
    # number of bits.
    value |= 1 << (nbits - 1)

    return value


def read_random_odd_int(nbits):
    """Reads a random odd integer of approximately nbits bits.

    >>> read_random_odd_int(512) & 1
    1
    """

    value = read_random_int(nbits)

    # Make sure it's odd
    return value | 1


def randint(maxvalue):
    """Returns a random integer x with 1 <= x <= maxvalue

    May take a very long time in specific situations. If maxvalue needs N bits
    to store, the closer maxvalue is to (2 ** N) - 1, the faster this function
    is.
    """

    bit_size = maxvalue.bit_length()

    tries = 0
    while True:
        value = read_random_int(bit_size)
        if value <= maxvalue:
            break

        if tries % 10 == 0 and tries:
            # After a lot of tries to get the right number of bits but still
            # smaller than maxvalue, decrease the number of bits by 1. That'll
            # dramatically increase the chances to get a large enough number.
            bit_size -= 1
        tries += 1

    return value
