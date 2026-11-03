"""Original-arcade-inspired main menu with compatible click targets."""

import pygame
from ui.arcade import (BLACK, CYAN, PINK, WHITE, YELLOW,
                       arcade_text, draw_border, draw_decorations)

screen: pygame.Surface | None = None


def set_screen(value: pygame.Surface) -> None:
    """Store the screen used by legacy menu entry points."""
    global screen
    screen = value


def color(x: str) -> tuple[int, int, int] | str:
    """Support the legacy palette accessor."""
    palette = {"pacman_color": YELLOW, "white": WHITE,
               "yellwo": YELLOW, "black": BLACK}
    return palette.get(x, "chose a color")


def fontsize(x: int) -> pygame.font.Font:
    """Create a menu font."""
    return pygame.font.Font(None, x)


def cord(x: int, y: int) -> tuple[int, int]:
    """Return screen coordinates."""
    return (x, y)


def window_size() -> tuple[int, int]:
    """Use the original project's window dimensions."""
    return (1000, 800)


def background() -> None:
    """Render a pure-black arcade cabinet and glowing maze frame."""
    if screen is None:
        return
    screen.fill(BLACK)
    draw_border(screen, pygame.Rect(160, 38, 680, 718))
    arcade_text(screen, "1UP     HIGH SCORE     2UP", 17, 65, WHITE)
    arcade_text(screen, "00         10000         00", 19, 91, WHITE)


def title() -> None:
    """Render the arcade yellow Pac-Man marqueé."""
    if screen is None:
        return
    arcade_text(screen, "PAC-MAN", 85, 142, YELLOW)
    draw_decorations(screen, 295)


_OPTIONS = (("START GAME", "start", 375),
            ("HIGH SCORES", "highscores", 455),
            ("INSTRUCTIONS", "instructions", 535),
            ("EXIT", "exit", 615))


def menu() -> None:
    """Render selectable menu entries without changing input semantics."""
    if screen is None:
        return
    mouse = pygame.mouse.get_pos()
    for text, _, y in _OPTIONS:
        selected = 300 <= mouse[0] <= 700 and y-15 <= mouse[1] <= y+55
        arcade_text(screen, text, 34, y, YELLOW if selected else WHITE)
        if selected:
            arcade_text(screen, "<                 >", 28, y+3, CYAN)
    arcade_text(screen, "PUSH START BUTTON", 17, 700, PINK)


def button(event: pygame.event.Event) -> str | None:
    """Map mouse clicks to the same actions as the original UI."""
    if event.type == pygame.QUIT:
        return "exit"
    if event.type != pygame.MOUSEBUTTONDOWN:
        return None
    x, y = event.pos
    if 300 <= x <= 700:
        for _, action, top in _OPTIONS:
            if top-15 <= y <= top+55:
                return action
    return None
