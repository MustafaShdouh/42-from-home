"""Instructions screen rendering and input handling."""

import pygame


def instructions(screen: pygame.Surface) -> None:
    """Draw controls, rules, and power-up instructions."""
    screen.fill((0, 0, 0))

    yellow = (255, 255, 0)
    white = (255, 255, 255)
    blue = (30, 65, 255)

    title_font = pygame.font.Font(None, 80)
    text_font = pygame.font.Font(None, 34)
    back_font = pygame.font.Font(None, 48)

    title = title_font.render("INSTRUCTIONS", True, yellow)
    title_x = (screen.get_width() - title.get_width()) // 2
    screen.blit(title, (title_x, 55))

    lines = [
        "MOVE: ARROW KEYS OR WASD",
        "PAUSE / RESUME: P",
        "EAT ALL PACGUMS TO COMPLETE THE LEVEL",
        "SUPER-PACGUMS MAKE GHOSTS EDIBLE FOR A SHORT TIME",
        "AVOID GHOSTS WHILE THEY ARE NOT EDIBLE",
        "KEEP YOUR SCORE AND REMAINING LIVES BETWEEN LEVELS",
        "CHEATS: C = INVINCIBILITY, N = SKIP LEVEL, F = FREEZE GHOSTS",
    ]

    y = 180
    for line in lines:
        text = text_font.render(line, True, white)
        text_x = (screen.get_width() - text.get_width()) // 2
        screen.blit(text, (text_x, y))
        y += 58

    back = back_font.render("BACK", True, blue)
    back_x = (screen.get_width() - back.get_width()) // 2
    screen.blit(back, (back_x, 650))


def instructions_button(event: pygame.event.Event) -> str | None:
    """Return 'back' when the back option is selected."""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return "back"

    if event.type != pygame.MOUSEBUTTONDOWN:
        return None

    mouse_x, mouse_y = event.pos
    if 400 <= mouse_x <= 600 and 630 <= mouse_y <= 710:
        return "back"

    return None
