"""Keyboard controlled character movement for Drill 9."""

from pathlib import Path

import pico2d as p2d

from movement import CANVAS_HEIGHT, CANVAS_WIDTH, SPRITE_SIZE, Character

KEY_TO_DIRECTION = {
    p2d.SDLK_LEFT: "left",
    p2d.SDLK_RIGHT: "right",
    p2d.SDLK_UP: "up",
    p2d.SDLK_DOWN: "down",
}


def main() -> None:
    asset_dir = Path(__file__).resolve().parent
    p2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        background = p2d.load_image(str(asset_dir / "TUK_GROUND.png"))
        sprite = p2d.load_image(str(asset_dir / "animation_sheet.png"))
        character = Character()
        running = True

        while running:
            for event in p2d.get_events():
                if event.type == p2d.SDL_QUIT:
                    running = False
                elif event.type == p2d.SDL_KEYDOWN and event.key == p2d.SDLK_ESCAPE:
                    running = False
                elif event.type == p2d.SDL_KEYDOWN and event.key in KEY_TO_DIRECTION:
                    character.press(KEY_TO_DIRECTION[event.key])

            p2d.clear_canvas()
            background.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
            sprite.clip_draw(0, 300, SPRITE_SIZE, SPRITE_SIZE, character.x, character.y)
            p2d.update_canvas()
            p2d.delay(0.01)
    finally:
        p2d.close_canvas()


if __name__ == "__main__":
    main()
