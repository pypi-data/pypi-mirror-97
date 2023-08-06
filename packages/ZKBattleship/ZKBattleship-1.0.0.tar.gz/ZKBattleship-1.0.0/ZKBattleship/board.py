import pedersen
import pickle
import bitproof
import unittest
import time

class Board:
    """Board class that all others inherit from"""
    LETTERS = {'a': 1, 'b': 2, 'c': 3, 'd': 4,
               'e': 5, 'f': 6, 'g': 7, 'h': 8}

    def __init__(self):
        """Initizializes normal board with size 8 x 8 filled with zeroes"""
        self.board = [0 for _ in range(64)]

    def get_spot_index(self, spot):
        """Translates a battleship coordinate to a index"""
        if (int(spot[1]) < 1 or int(spot[1]) > 8
            or spot[0] not in self.LETTERS):
            raise ValueError
        return (self.LETTERS[spot[0].lower()] -  1) * 8 + int(spot[1]) - 1

    def get_spot(self, spot):
        """Returns spot value at battleship coordinate"""
        return self.board[self.get_spot_index(spot)]

class CommitmentBoard(Board):
    """Board that also has a parallel commitment board"""

    def __init__(self):
        """Initializes three boards and commitment generator
        The first board is the normal board
        The second board is the commitment board for one's own use
        The third board is the public commitment board for opponent use
        """
        super().__init__()
        self.commitment_generator = pedersen.Pedersen(64)
        self.commitment_board = [None for _ in range(64)]
        self.public_commitments = [0 for _ in range(64)]

    def update_commitments(self):
        """Updates the commitments on the commitment board and public board"""
        self.commitment_board = [self.commitment_generator.commit(x)
                              for x in self.board]
        self.public_commitments = [x.c for x in self.commitment_board]

    def send_commitments(self):
        """Returns the public commitments"""
        return self.public_commitments

    def send_sum_proof(self):
        """Sends the proof that the board squares add to eight"""
        return pedersen.Pedersen.add_commitments(
            self.commitment_generator.state, *self.commitment_board)

    def send_bit_proof(self):
        """Sends the proof that all board values are bits"""
        return [bitproof.bitproof(x, y, self.commitment_generator.state)
                for x, y in zip(self.board, self.commitment_board)]

    def send_initial(self):
        """Sends all proofs"""
        return pickle.dumps((self.send_commitments(),
                            self.send_sum_proof(),
                            self.send_bit_proof(),
                            self.commitment_generator.state))

    def get_commitment(self, spot):
        """Gets the commitment at spot"""
        return self.commitment_board[self.get_spot_index(spot)]

class ShipBoard(CommitmentBoard):
    """Board to hold ships in"""

    def input_board(self, f = None, t = 8):
        """Asks player to input ships onto board with index protections"""
        i = 0
        while i < t:
            print(self)
            print(str(i) + (" spot " if i == 1 else " spots ") + "taken")
            a = input()
            try:
                if self.get_spot(a) == 1:
                    print(f"Spot at {a} removed")
                    i -= 1
                else:
                    print(f"Spot at {a} added")
                    i += 1
                self.set_spot(a)
            except ValueError:
                print(f"{a} is not a spot on the board")
            except IndexError:
                print(f"{a} is not a spot on the board")
            time.sleep(1.5)
            if f:
                _ = f()


    def __repr__(self):
        """Returns the board as a string"""
        a = ' '
        for i in range(8):
            a += ' ' + str(i + 1)
        it = iter(self.LETTERS.items())
        for i, s in enumerate(self.board):
            a += '\n' + next(it)[0] + ' ' if (i) % 8 == 0 else ' '
            a += 'X' if s == 1 else '-'
        return a

    def set_spot(self, *spots):
        """Toggles an arbitray number of spots
        Used primarily for testing
        """
        for spot in spots:
            self.board[self.get_spot_index(spot)] ^= 1


class GuessBoard(Board):
    """Board for holding players guesses and opponents responses"""

    def __repr__(self):
        """Returns board as string"""
        a = ' '
        for i in range(8):
            a += ' ' + str(i + 1)
        it = iter(self.LETTERS.items())
        for i, s in enumerate(self.board):
            a += '\n' + next(it)[0] + ' ' if (i) % 8 == 0 else ' '
            a += 'X' if s == 2 else 'x' if s == 1 else '-'
        return a

    def set_spot(self, spot, value):
        """Sets spot to given value"""
        self.board[self.get_spot_index(spot)] = value




class TestProofs(unittest.TestCase):

    def test(self):
        a = ShipBoard()
        a.set_spot("a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8")
        a.update_commitments()
        b = a.send_initial()
        c = pickle.loads(b)
        self.assertTrue(pedersen.Pedersen.verify(8, c[1], c[3]))
        self.assertFalse(pedersen.Pedersen.verify(9, c[1], c[3]))
        for x, y in zip(c[0], c[2]):
            self.assertTrue(bitproof.verify(x, c[3], y))

if __name__ == "__main__":
    unittest.main()
