"""Pause-menu rendering and input handling."""

import pygame


def pause_menu(screen: pygame.Surface) -> None:
    """Draw the pause overlay with resume and main-menu options."""
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 210))
    screen.blit(overlay, (0, 0))

    yellow = (255, 255, 0)
    white = (255, 255, 255)

    title_font = pygame.font.Font(None, 80)
    menu_font = pygame.font.Font(None, 55)

    title = title_font.render(
        "PAUSED",
        True,
        yellow
    )

    resume = menu_font.render(
        "RESUME",
        True,
        white
    )

    main_menu = menu_font.render(
        "RETURN TO MAIN MENU",
        True,
        white
    )

    screen_width = screen.get_width()

    title_x = (
        screen_width - title.get_width()
    ) // 2

    resume_x = (
        screen_width - resume.get_width()
    ) // 2

    main_menu_x = (
        screen_width - main_menu.get_width()
    ) // 2

    screen.blit(
        title,
        (title_x, 200)
    )

    screen.blit(
        resume,
        (resume_x, 350)
    )

    screen.blit(
        main_menu,
        (main_menu_x, 450)
    )


def pause_button(event: pygame.event.Event) -> str | None:
    """Return the pause-menu action selected by the player."""
    if event.type != pygame.MOUSEBUTTONDOWN:
        return None

    mouse_x, mouse_y = event.pos

    if 350 <= mouse_x <= 650 and 330 <= mouse_y <= 410:
        return "resume"

    if 250 <= mouse_x <= 750 and 430 <= mouse_y <= 510:
        return "menu"

    return None
