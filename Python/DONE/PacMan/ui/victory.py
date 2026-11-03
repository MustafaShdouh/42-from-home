"""Victory screen rendering and player-name input."""

from typing import Any

import pygame


def victory(
    screen: pygame.Surface,
    game: Any,
    player_name: str,
) -> None:
    """Draw the victory message, final score, and name-entry prompt."""
    screen.fill((0, 0, 0))

    yellow = (255, 255, 0)
    white = (255, 255, 255)

    title_font = pygame.font.Font(None, 100)
    score_font = pygame.font.Font(None, 60)
    text_font = pygame.font.Font(None, 42)

    title = title_font.render("VICTORY!", True, yellow)
    message = text_font.render("CONGRATULATIONS!", True, white)
    score = score_font.render(
        f"FINAL SCORE: {game.score}", True, white
    )
    prompt = text_font.render(
        "ENTER NAME (MAX 10):", True, white
    )
    name = text_font.render(
        player_name if player_name else "_", True, yellow
    )
    save = text_font.render(
        "PRESS ENTER TO SAVE", True, white
    )

    title_x = (screen.get_width() - title.get_width()) // 2
    message_x = (screen.get_width() - message.get_width()) // 2
    score_x = (screen.get_width() - score.get_width()) // 2
    prompt_x = (screen.get_width() - prompt.get_width()) // 2
    name_x = (screen.get_width() - name.get_width()) // 2
    save_x = (screen.get_width() - save.get_width()) // 2

    screen.blit(title, (title_x, 120))
    screen.blit(message, (message_x, 230))
    screen.blit(score, (score_x, 310))
    screen.blit(prompt, (prompt_x, 430))
    screen.blit(name, (name_x, 490))
    screen.blit(save, (save_x, 580))


def victory_input(
    event: pygame.event.Event,
    player_name: str,
) -> tuple[str, bool]:
    """Update the player name and report when Enter submits it."""
    if event.type != pygame.KEYDOWN:
        return player_name, False

    if event.key == pygame.K_BACKSPACE:
        return player_name[:-1], False

    if event.key == pygame.K_RETURN:
        return player_name, True

    char = event.unicode
    if len(player_name) < 10 and (char.isalnum() or char == " "):
        return player_name + char, False

    return player_name, False
