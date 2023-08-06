import secrets
import hashlib
import pickle
import dataclasses
import pedersen
import unittest

def bitproof(message, commitment, state):
    """Generates bit proof"""
    r = secrets.randbelow(state.p)
    if message == 0:
        e1 = secrets.randbelow(state.p)
        y1 = secrets.randbelow(state.p)
        x0 = pow(state.h, r, state.p)
        x1 = (pow(state.h, y1, state.p)
              * pow(commitment.c * pow(state.g, -1, state.p), -e1, state.p)
              % state.p)
        e = hash_int((x0, x1)) % state.p
        e0 = (e - e1) % state.p
        y0 = (r + commitment.r * e0) % (state.p - 1)
    elif message == 1:
        e0 = secrets.randbelow(state.p)
        y0 = secrets.randbelow(state.p)
        x1 = pow(state.h, r, state.p)
        x0 = (pow(state.h, y0, state.p)
              * pow(commitment.c, -e0, state.p) % state.p)
        e = hash_int((x0, x1)) % state.p
        e1 = (e - e0) % state.p
        y1 = (r + commitment.r * e1) % (state.p - 1)
    else:
        raise ValueError
    return Output(e, e0, e1, x0, x1, y0, y1)


@dataclasses.dataclass
class Output:
    """Holds public output of bit proof"""
    e: int
    e0: int
    e1: int
    x0: int
    x1: int
    y0: int
    y1: int


def hash_int(x):
    """Pickles, hashes, and returns input as an integer"""
    return int.from_bytes(hashlib.blake2b(pickle.dumps(x)).digest(),"big")

def verify(c, p_state, bp_state):
    """Verifies bit proof"""
    c_a = (bp_state.e
           == hash_int((bp_state.x0, bp_state.x1)) % p_state.p)
    c_b = (bp_state.x1
           * pow(c * pow(p_state.g, -1, p_state.p), bp_state.e1, p_state.p)
           % p_state.p
           == pow(p_state.h, bp_state.y1, p_state.p))
    c_c = (bp_state.x0 * pow(c, bp_state.e0, p_state.p) % p_state.p
           == pow(p_state.h, bp_state.y0, p_state.p))
    c_d = ((bp_state.e1 + bp_state.e0) % p_state.p
           == bp_state.e)
    return c_a and c_b and c_c and c_d


class TestBitProof(unittest.TestCase):

    def test0(self):
        a = pedersen.Pedersen(64)
        b = a.commit(0)
        c = bitproof(0, b, a.state)
        d = bitproof(1, b, a.state)
        self.assertTrue(verify(b.c, a.state, c))
        self.assertFalse(verify(b.c, a.state, d))

    def test1(self):
        a = pedersen.Pedersen(64)
        b = a.commit(1)
        c = bitproof(0, b, a.state)
        d = bitproof(1, b, a.state)
        self.assertTrue(verify(b.c, a.state, d))
        self.assertFalse(verify(b.c, a.state, c))


if __name__ == "__main__":
    unittest.main()

