import unittest
from types import SimpleNamespace
from unittest import mock

import move_character_with_key as app


class AppTests(unittest.TestCase):
    def test_key_press_release_switches_sprite_rows(self):
        background = mock.Mock()
        sprite = mock.Mock()
        events = [
            [SimpleNamespace(type=app.p2d.SDL_KEYDOWN, key=app.p2d.SDLK_LEFT)],
            [SimpleNamespace(type=app.p2d.SDL_KEYUP, key=app.p2d.SDLK_LEFT)],
            [SimpleNamespace(type=app.p2d.SDL_KEYDOWN, key=app.p2d.SDLK_ESCAPE)],
        ]
        with mock.patch.multiple(
            app.p2d,
            open_canvas=mock.DEFAULT,
            close_canvas=mock.DEFAULT,
            load_image=mock.DEFAULT,
            get_events=mock.DEFAULT,
            get_time=mock.DEFAULT,
            clear_canvas=mock.DEFAULT,
            update_canvas=mock.DEFAULT,
            delay=mock.DEFAULT,
        ) as patched:
            patched["load_image"].side_effect = [background, sprite]
            patched["get_events"].side_effect = events
            patched["get_time"].side_effect = [0.0, 0.1, 0.2]
            app.main()

        patched["open_canvas"].assert_called_once_with(1280, 1024)
        self.assertEqual(background.draw.call_count, 2)
        self.assertEqual(sprite.clip_draw.call_count, 2)
        first, second = [call.args for call in sprite.clip_draw.call_args_list]
        self.assertEqual(first[1], 0)
        self.assertEqual(second[1], 200)
        self.assertLess(first[4], 640)
        self.assertEqual(second[4], first[4])
        patched["close_canvas"].assert_called_once()

    def test_canvas_closes_when_asset_loading_fails(self):
        with mock.patch.object(app.p2d, "open_canvas") as open_canvas, \
             mock.patch.object(app.p2d, "close_canvas") as close_canvas, \
             mock.patch.object(app.p2d, "load_image", side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                app.main()
        open_canvas.assert_called_once_with(1280, 1024)
        close_canvas.assert_called_once()


if __name__ == "__main__":
    unittest.main()
