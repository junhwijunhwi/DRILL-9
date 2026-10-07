"""Drill 9 character movement and sprite state, independent of the window."""

from math import hypot
from dataclasses import dataclass, field

CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 1024
SPRITE_SIZE = 100
FRAME_COUNT = 8
FRAME_DURATION = 0.1
MOVE_SPEED = 240.0

DIRECTIONS = frozenset({"left", "right", "up", "down"})


def key_axis(pressed):
    """Return signed horizontal and vertical axes from pressed directions."""
    if not pressed <= DIRECTIONS:
        raise ValueError("unknown direction")
    horizontal = int("right" in pressed) - int("left" in pressed)
    vertical = int("up" in pressed) - int("down" in pressed)
    return horizontal, vertical


def movement_vector(pressed):
    """Return a unit direction vector, or zero when the keys cancel."""
    horizontal, vertical = key_axis(pressed)
    length = hypot(horizontal, vertical)
    if not length:
        return 0.0, 0.0
    return horizontal / length, vertical / length


@dataclass
class Character:
    x: float = CANVAS_WIDTH / 2
    y: float = CANVAS_HEIGHT / 2
    facing: str = "right"
    pressed: set[str] = field(default_factory=set)
    moving: bool = False
    frame: int = 0
    animation_elapsed: float = 0.0

    def press(self, direction: str) -> None:
        if direction not in DIRECTIONS:
            raise ValueError("unknown direction")
        self.pressed.add(direction)

    def release(self, direction: str) -> None:
        if direction not in DIRECTIONS:
            raise ValueError("unknown direction")
        self.pressed.discard(direction)
