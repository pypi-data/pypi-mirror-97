import secrets
import unittest
import math

def is_prime_helper(m, k, n):
    """Returns if value is prime using Miller-Rabin primality test"""
    a = secrets.randbelow(n - 5) + 2
    b = pow(a, m, n)
    if (b == 1 or b == n - 1):
        return True
    for _ in range(k):
        b = pow(b, 2, n)
        if (b % n == 1):
            return False
        if (b % n == n - 1):
            return True
    return True


def is_prime(n, s = 128):
    """Returns if value is prime.
    Divisibility test for prime numbers under 100
    Fermat primality test for a = 2 and a = 3
    Miller-Rabin primality test repeating s times
    """
    PRIME = {2, 3, 5, 7, 11, 13, 17, 19, 23,
             29, 31, 37, 41, 43, 47, 53, 59,
             61, 67, 71, 73, 79, 83, 89, 97}
    if n < 100:
        return n in PRIME
    else:
        for x in PRIME:
            if n % x == 0:
                return False
    if (pow(2, n - 1, n) != 1):
        return False
    if (pow(3, n - 1, n) != 1):
        return False
    m = n - 1
    k = 0
    while m % 2 == 0:
        k += 1
        m //= 2
    m = int(m)
    for l in range(s):
        if not is_prime_helper(m, k, n):
            return False
    return True


def prime_randbits(bit_length):
    """Returns prime number of bits: bit_length"""
    x = secrets.randbits(bit_length - 1) * 2 + 1
    while not is_prime(x):
        x += 2
    return x


def safe_prime_randbits(bit_length):
    """Returns safe prime number of bits: bit_length
    Safe primes are primes of which x * 2 + 1 is also a prime
    """
    x = secrets.randbits(bit_length - 1) * 2 + 1
    while not is_prime(x) or not is_prime(x * 2 + 1):
        x += 2
    return x


def schnorr_prime_randbits(bit_length):
    """Returns schnorr prime number of bits: bit_length
    Schnorr primes are primes of which x * 4 + 1 is also a prime
    """
    x = secrets.randbits(bit_length - 1) * 2 + 1
    while not is_prime(x) or not is_prime(x * 4 + 1):
        x += 2
    return x


def prime_randbelow(n):
    """Returns prime number less than: n"""
    x = secrets.randbelow(n)
    while not is_prime(x):
        x += 2
        if x > n:
            x = secrets.randbelow(n)
            continue
    return x

def primality_check(x):
    """Deterministically checks if x is prime"""
    for i in range(2, math.ceil(math.sqrt(x))):
        if x % i == 0:
            return False
    return True

class TestPrime(unittest.TestCase):

    def test_randbelow(self):
        for i in range(500):
            self.assertTrue(primality_check(prime_randbelow(2**16)))

    def test_schnorr_prime_randbits(self):
        for i in range(500):
            a = schnorr_prime_randbits(16)
            self.assertTrue(primality_check(a))
            self.assertTrue(primality_check(a * 4 + 1))

    def test_safe_prime_randbits(self):
        for i in range(500):
            a = safe_prime_randbits(16)
            self.assertTrue(primality_check(a))
            self.assertTrue(primality_check(a * 2 + 1))

    def test_prime_randbits(self):
        for i in range(500):
            self.assertTrue(primality_check(prime_randbits(16)))

if __name__ == "__main__":
    unittest.main()
