import unittest

from movement import Character, key_axis


class InputTests(unittest.TestCase):
    def test_opposite_keys_cancel_on_each_axis(self):
        self.assertEqual(key_axis({"left", "right", "up"}), (0, 1))
        self.assertEqual(key_axis({"up", "down"}), (0, 0))

    def test_releasing_one_key_keeps_other_pressed(self):
        character = Character()
        character.press("left")
        character.press("up")
        character.release("left")
        self.assertEqual(key_axis(character.pressed), (0, 1))


if __name__ == "__main__":
    unittest.main()
