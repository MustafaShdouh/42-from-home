"""Highscore screen rendering and input handling."""

from typing import Any

import pygame


def highscore_view(screen: pygame.Surface, game: Any) -> None:
    """Draw the top ten highscores stored by the core engine."""
    screen.fill((0, 0, 0))

    yellow = (255, 255, 0)
    white = (255, 255, 255)
    blue = (30, 65, 255)

    title_font = pygame.font.Font(None, 80)
    score_font = pygame.font.Font(None, 40)
    back_font = pygame.font.Font(None, 48)

    title = title_font.render("HIGHSCORES", True, yellow)
    title_x = (screen.get_width() - title.get_width()) // 2
    screen.blit(title, (title_x, 55))

    highscores = list(game.highscores[:10])

    if not highscores:
        empty = score_font.render("NO HIGHSCORES YET", True, white)
        empty_x = (screen.get_width() - empty.get_width()) // 2
        screen.blit(empty, (empty_x, 220))
    else:
        y = 160
        for index, entry in enumerate(highscores, start=1):
            name = str(entry.get("name", "ANONYMOUS"))[:10]
            score = entry.get("score", 0)
            line = score_font.render(
                f"{index:>2}. {name:<10}  {score}", True, white
            )
            line_x = (screen.get_width() - line.get_width()) // 2
            screen.blit(line, (line_x, y))
            y += 45

    back = back_font.render("BACK", True, blue)
    back_x = (screen.get_width() - back.get_width()) // 2
    screen.blit(back, (back_x, 680))


def highscore_button(event: pygame.event.Event) -> str | None:
    """Return 'back' when the player leaves the highscore screen."""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return "back"

    if event.type != pygame.MOUSEBUTTONDOWN:
        return None

    mouse_x, mouse_y = event.pos
    if 400 <= mouse_x <= 600 and 660 <= mouse_y <= 740:
        return "back"

    return None
