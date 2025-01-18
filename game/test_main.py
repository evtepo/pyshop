import unittest

from main import get_score


game_stamps = [
    {"offset": 12130, "score": {"away": 0, "home": 0}},
    {"offset": 12131, "score": {"away": 0, "home": 1}},
    {"offset": 12152, "score": {"away": 1, "home": 2}},
    {"offset": 12160, "score": {"away": 2, "home": 3}},
]


class TestScore(unittest.TestCase):
    def test_game_stamps(self):
        self.assertEqual(get_score(game_stamps, 12160), (3, 2))
        self.assertEqual(get_score([], 12160), (0, 0))

    def test_offset(self):
        self.assertEqual(get_score(game_stamps, 12131), (1, 0))
        self.assertEqual(get_score(game_stamps, 1), (0, 0))
        self.assertEqual(get_score(game_stamps, -10), (0, 0))

    def test_invalid_inputs(self):
        self.assertEqual(get_score(None, 10), (0, 0))
        self.assertEqual(get_score(game_stamps, "invalid_offset"), (0, 0))


if __name__ == "__main__":
    unittest.main()
