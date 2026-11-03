"""Classic arcade-inspired maze, sprite, and score rendering."""

import math
from typing import Any
import pygame
from ui.arcade import (BLACK, BLUE, CYAN, ORANGE, PINK, RED,
                       WHITE, YELLOW, draw_ghost, draw_pacman)


def game_view(screen: pygame.Surface, game: Any) -> None:
    """Draw the core game state while leaving all game mechanics untouched."""
    screen.fill(BLACK)
    if not game.maze or not game.maze[0]:
        return
    rows, columns = len(game.maze), len(game.maze[0])
    hud_height, footer_height = 77, 65
    cell = max(1, min((screen.get_width()-60)//columns,
                      (screen.get_height()-hud_height-footer_height)//rows))
    width, height = columns*cell, rows*cell
    ox = (screen.get_width()-width)//2
    oy = hud_height+(screen.get_height()-hud_height-footer_height-height)//2
    maze = game.maze

    # Highlight the solid 42-shaped wall mass generated in the maze center.
    # This is purely visual: it does not edit the maze or its collisions.
    # The solid logo has broad 3x3 wall areas; ordinary thin maze walls do not.
    logo_core = set()
    for y in range(max(1, rows // 4), min(rows - 1, rows * 3 // 4)):
        for x in range(max(1, columns // 4),
                       min(columns - 1, columns * 3 // 4)):
            if all(maze[ny][nx] == 1
                   for ny in range(y - 1, y + 2)
                   for nx in range(x - 1, x + 2)):
                logo_core.add((x, y))

    # Include bordering wall cells so the solid logo is a continuous shape.
    logo_wall = set()
    for x, y in logo_core:
        for ny in range(y - 1, y + 2):
            for nx in range(x - 1, x + 2):
                if maze[ny][nx] == 1:
                    logo_wall.add((nx, ny))
    for x, y in logo_wall:
        pygame.draw.rect(screen, (9, 18, 78),
                         (ox + x * cell, oy + y * cell, cell, cell))

    # Classic blue line-art: draw boundaries between wall and corridor,
    # rather than filling the cells with chunky blue rectangles.
    thickness = max(2, cell//9)
    for y, row in enumerate(maze):
        for x, value in enumerate(row):
            px, py = ox+x*cell, oy+y*cell
            if value == 1:
                if y == 0 or maze[y-1][x] != 1:
                    pygame.draw.line(screen, BLUE, (px, py),
                                     (px+cell, py), thickness)
                if y == rows-1 or maze[y+1][x] != 1:
                    pygame.draw.line(screen, BLUE, (px, py+cell),
                                     (px+cell, py+cell), thickness)
                if x == 0 or maze[y][x-1] != 1:
                    pygame.draw.line(screen, BLUE, (px, py),
                                     (px, py+cell), thickness)
                if x == columns-1 or maze[y][x+1] != 1:
                    pygame.draw.line(screen, BLUE, (px+cell, py),
                                     (px+cell, py+cell), thickness)
            elif value in (2, 3):
                center = (px+cell//2, py+cell//2)
                radius = max(2, cell//11) if value == 2 else max(4, cell//4)
                if value == 3 and (pygame.time.get_ticks()//270) % 2:
                    radius = max(2, radius-2)
                pygame.draw.circle(screen, (255, 184, 181), center, radius)

    player_x = float(getattr(game.player, "render_x", game.player.x))
    player_y = float(getattr(game.player, "render_y", game.player.y))
    pulse = (math.sin(pygame.time.get_ticks()/90)+1)/2
    draw_pacman(screen, round(ox+(player_x+.5)*cell),
                round(oy+(player_y+.5)*cell), max(3, cell*2//5),
                game.player.direction, .08+.40*pulse)

    colors = {"RED": RED, "PINK": PINK, "CYAN": CYAN, "ORANGE": ORANGE}
    for ghost in game.ghosts:
        gx = float(getattr(ghost, "render_x", ghost.x))
        gy = float(getattr(ghost, "render_y", ghost.y))
        x = round(ox+(gx+.5)*cell)
        y = round(oy+(gy+.5)*cell)
        if ghost.mode == "DEAD":
            for shift in (-cell//9, cell//9):
                pygame.draw.ellipse(screen, WHITE,
                                    (x+shift-2, y-4, 5, 7))
                pygame.draw.circle(screen, BLUE, (x+shift, y), 2)
        else:
            draw_ghost(screen, x, y, max(4, cell*2//5),
                       colors.get(ghost.color, RED),
                       ghost.mode == "FRIGHTENED")

    font = pygame.font.SysFont("dejavusansmono", 20, bold=True)

    def print_at(message: str, x: int, y: int,
                 color: tuple[int, int, int] = WHITE) -> None:
        """Render crisp retro score text."""
        screen.blit(font.render(message, False, color), (x, y))

    print_at("1UP", ox, 12)
    print_at(f"{game.score:07d}", ox, 38)
    print_at(f"LEVEL {game.level:02d}", ox+width//2-65, 18, CYAN)
    print_at(f"TIME {max(0, int(game.time_remaining)):03d}",
             ox+width-110, 40, YELLOW)
    print_at("LIVES", ox, screen.get_height()-47, YELLOW)
    for i in range(min(12, max(0, int(game.lives)))):
        draw_pacman(screen, ox+115+30*i,
                    screen.get_height()-35, 10, "RIGHT", .28)
    print_at("P - PAUSE", ox+width-135, screen.get_height()-44, PINK)
