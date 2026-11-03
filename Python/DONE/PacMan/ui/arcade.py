"""Shared retro arcade visual elements, drawn with pygame primitives."""

import math
import pygame

BLACK = (0, 0, 0)
BLUE = (30, 65, 255)
YELLOW = (255, 230, 28)
WHITE = (245, 245, 245)
PINK = (255, 170, 190)
RED = (255, 40, 48)
CYAN = (40, 235, 245)
ORANGE = (255, 173, 50)


def arcade_text(surface: pygame.Surface, message: str, size: int,
                y: int, color: tuple[int, int, int] = WHITE) -> pygame.Rect:
    """Center a brightly colored arcade-style heading on the screen."""
    font = pygame.font.SysFont("dejavusansmono", size, bold=True)
    rendered = font.render(message, False, color)
    rect = rendered.get_rect(centerx=surface.get_width() // 2, top=y)
    surface.blit(rendered, rect)
    return rect


def draw_pacman(surface: pygame.Surface, x: int, y: int,
                radius: int, direction: str = "RIGHT",
                mouth_open: float = 0.33) -> None:
    """Draw an animated wedge-mouthed classic yellow Pac-Man."""
    radius = max(radius, 3)
    angle = {"RIGHT": 0, "DOWN": 90, "LEFT": 180,
             "UP": 270}.get(direction, 0)
    half_gap = 5 + 39 * mouth_open
    points = [(x, y)]
    for deg in range(0, 65):
        a = math.radians(angle + half_gap +
                         (360 - 2 * half_gap) * deg / 64)
        points.append((int(x + radius * math.cos(a)),
                       int(y + radius * math.sin(a))))
    pygame.draw.polygon(surface, YELLOW, points)


def draw_ghost(surface: pygame.Surface, x: int, y: int,
               radius: int, color: tuple[int, int, int],
               frightened: bool = False, phase: int = 0) -> None:
    """Render a rounded ghost, scalloped hem, and directional eyes."""
    r = max(4, radius)
    if frightened:
        color = (35, 45, 235)
    pygame.draw.circle(surface, color, (x, y - r // 4), r)
    pygame.draw.rect(surface, color, (x-r, y-r//4, 2*r, r + r//2))
    foot_y = y + r + r//4
    for n in range(4):
        foot_x = x - r + (2*n+1)*r//4
        pygame.draw.circle(surface, color, (foot_x, foot_y),
                           max(2, r//4))
    if frightened:
        for dx in (-r//3, r//3):
            pygame.draw.circle(surface, WHITE, (x+dx, y-r//3),
                               max(1, r//9))
        pygame.draw.lines(surface, WHITE, False,
                          [(x-r//2+i*r//4,
                            y+r//2+(2 if i % 2 else -2))
                           for i in range(5)], max(1, r//8))
    else:
        for dx in (-r//3, r//3):
            pygame.draw.ellipse(surface, WHITE,
                                (x+dx-r//4, y-r//2,
                                 max(3, r//2), max(4, 3*r//4)))
            pygame.draw.circle(surface, (25, 65, 225),
                               (x+dx, y-r//5), max(2, r//6))


def draw_decorations(surface: pygame.Surface, y: int) -> None:
    """Draw a classic character parade under the title."""
    cx = surface.get_width() // 2
    draw_pacman(surface, cx-145, y, 22, "RIGHT", .33)
    for idx, color in enumerate((RED, PINK, CYAN, ORANGE)):
        draw_ghost(surface, cx-62+idx*53, y, 19, color)


def draw_border(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draw a blue double-line arcade cabinet style frame."""
    pygame.draw.rect(surface, BLUE, rect, 3, border_radius=13)
    pygame.draw.rect(surface, BLUE, rect.inflate(-13, -13), 2,
                     border_radius=8)
