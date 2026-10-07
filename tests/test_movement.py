import unittest
from math import hypot

from movement import CANVAS_HEIGHT, CANVAS_WIDTH, SPRITE_SIZE, Character, MOVE_SPEED, key_axis


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


class MovementTests(unittest.TestCase):
    def test_each_axis_moves_at_configured_speed(self):
        for direction, expected in (
            ("left", (-MOVE_SPEED, 0)),
            ("right", (MOVE_SPEED, 0)),
            ("up", (0, MOVE_SPEED)),
            ("down", (0, -MOVE_SPEED)),
        ):
            with self.subTest(direction=direction):
                character = Character()
                start = character.x, character.y
                character.press(direction)
                character.update(1.0)
                displacement = character.x - start[0], character.y - start[1]
                self.assertEqual(displacement, expected)

    def test_diagonal_speed_matches_axis_speed(self):
        character = Character()
        start = character.x, character.y
        character.press("up")
        character.press("right")
        character.update(1.0)
        self.assertAlmostEqual(hypot(character.x - start[0], character.y - start[1]), MOVE_SPEED)

    def test_sprite_stays_inside_all_screen_edges(self):
        half = SPRITE_SIZE / 2
        for direction, coordinate, bound in (
            ("left", "x", half),
            ("right", "x", CANVAS_WIDTH - half),
            ("down", "y", half),
            ("up", "y", CANVAS_HEIGHT - half),
        ):
            with self.subTest(direction=direction):
                character = Character()
                character.press(direction)
                character.update(100.0)
                self.assertEqual(getattr(character, coordinate), bound)
                character.update(1.0)
                self.assertEqual(getattr(character, coordinate), bound)
                self.assertFalse(character.moving)


if __name__ == "__main__":
    unittest.main()
