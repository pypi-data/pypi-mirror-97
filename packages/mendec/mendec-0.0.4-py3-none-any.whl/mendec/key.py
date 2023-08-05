from logging import debug, info, error
from .utils import randint


def extended_gcd(a, b):
    """Returns a tuple (r, i, j) such that r = gcd(a, b) = ia + jb"""
    # r = gcd(a,b) i = multiplicitive inverse of a mod b
    #      or      j = multiplicitive inverse of b mod a
    # Neg return values for i or j are made positive mod b or a respectively
    # Iterateive Version is faster and uses much less stack space
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a  # Remember original a/b to remove
    ob = b  # negative values from return results
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob  # If neg wrap modulo orignal b
    if ly < 0:
        ly += oa  # If neg wrap modulo orignal a
    return a, lx, ly  # Return only positive values


class NotRelativePrimeError(ValueError):
    def __init__(self, a, b, d, msg=None):
        super(NotRelativePrimeError, self).__init__(
            msg or "%d and %d are not relatively prime, divider=%i" % (a, b, d)
        )
        self.a = a
        self.b = b
        self.d = d


def inverse(x, n):
    """Returns the inverse of x % n under multiplication, a.k.a x^-1 (mod n)

    >>> inverse(7, 4)
    3
    >>> (inverse(143, 4) * 143) % 4
    1
    """

    (divider, inv, _) = extended_gcd(x, n)

    if divider != 1:
        raise NotRelativePrimeError(x, n, divider)

    return inv


def find_p_q(nbits, getprime_func, accurate=True):
    total_bits = nbits * 2

    # Make sure that p and q aren't too close or the factoring programs can
    # factor n.
    shift = nbits // 16
    pbits = nbits + shift
    qbits = nbits - shift

    # Choose the two initial primes
    debug("find_p_q(%i): Finding p", nbits)
    p = getprime_func(pbits)
    debug("find_p_q(%i): Finding q", nbits)
    q = getprime_func(qbits)

    def is_acceptable(p, q):
        """Returns True iff p and q are acceptable:

        - p and q differ
        - (p * q) has the right nr of bits (when accurate=True)
        """

        if p == q:
            return False

        if not accurate:
            return True

        # Make sure we have just the right amount of bits
        found_size = (p * q).bit_length()
        return total_bits == found_size

    # Keep choosing other primes until they match our requirements.
    change_p = False
    while not is_acceptable(p, q):

        # Change p on one iteration and q on the other
        if change_p:
            debug("p and q not acceptable, finding p")
            p = getprime_func(pbits)
        else:
            debug("p and q not acceptable, finding q")
            q = getprime_func(qbits)

        change_p = not change_p

    # We want p > q as described on
    # http://www.di-mgt.com.au/rsa_alg.html#crt
    return max(p, q), min(p, q)


def calculate_keys_custom_exponent(p, q):
    """Calculates an encryption and a decryption key given p, q and an exponent,
    and returns them as a tuple (e, d)

    :param p: the first large prime
    :param q: the second large prime
    :param exponent: the exponent for the key; only change this if you know
        what you're doing, as the exponent influences how difficult your
        private key can be cracked. A very common choice for e is 65537.
    :type exponent: int

    """

    phi_n = (p - 1) * (q - 1)

    while 1:
        try:
            exponent = randint(phi_n)

            d = inverse(exponent, phi_n)
            break
        except NotRelativePrimeError as ex:
            error("{!r} try again".format(ex))

    if (exponent * d) % phi_n != 1:
        raise ValueError(
            "e (%d) and d (%d) are not mult. inv. modulo "
            "phi_n (%d)" % (exponent, d, phi_n)
        )

    return exponent, d


def gen_keys(nbits, getprime_func, accurate=True):
    i = 0
    while True:
        i += 1
        info("%r\tFind p, q", i)
        (p, q) = find_p_q(nbits // 2, getprime_func, accurate)
        try:
            info("\tCalc e, d")
            (e, d) = calculate_keys_custom_exponent(p, q)
            break
        except ValueError:
            pass

    return p, q, e, d


def newkeys(nbits, accurate=True, poolsize=1):

    if nbits < 16:
        raise ValueError("Key too small")

    if poolsize < 1:
        raise ValueError("Pool size (%i) should be >= 1" % poolsize)

    # Determine which getprime function to use
    if poolsize > 1:
        from .parallel import getprime
        from functools import partial

        getprime_func = partial(getprime, poolsize=poolsize)
    else:
        from .prime import getprime

        getprime_func = getprime

    # Generate the key components
    (p, q, e, d) = gen_keys(nbits, getprime_func, accurate=accurate)

    # Create the key objects
    n = p * q

    return n, e, d
