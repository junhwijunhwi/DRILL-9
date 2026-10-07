"""Drill 9 character movement and sprite state, independent of the window."""

from math import hypot
from dataclasses import dataclass, field

CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 1024
SPRITE_SIZE = 100
FRAME_COUNT = 8
FRAME_DURATION = 0.1
MOVE_SPEED = 240.0


def clamp(value: float, lower: float, upper: float) -> float:
    """Keep a sprite center within one canvas axis."""
    return max(lower, min(value, upper))

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

    def update(self, dt: float) -> None:
        """Advance the character using elapsed seconds."""
        if dt < 0:
            raise ValueError("elapsed time cannot be negative")

        horizontal, vertical = movement_vector(self.pressed)
        if horizontal < 0:
            self.facing = "left"
        elif horizontal > 0:
            self.facing = "right"

        old_position = self.x, self.y
        was_moving = self.moving
        half_sprite = SPRITE_SIZE / 2
        self.x = clamp(
            self.x + horizontal * MOVE_SPEED * dt,
            half_sprite,
            CANVAS_WIDTH - half_sprite,
        )
        self.y = clamp(
            self.y + vertical * MOVE_SPEED * dt,
            half_sprite,
            CANVAS_HEIGHT - half_sprite,
        )
        self.moving = (self.x, self.y) != old_position
        if self.moving != was_moving:
            self.animation_elapsed = 0.0
            self.frame = 0
        else:
            self.animation_elapsed += dt
            self.frame = int(self.animation_elapsed / FRAME_DURATION) % FRAME_COUNT
