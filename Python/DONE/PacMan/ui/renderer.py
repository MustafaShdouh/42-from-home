"""Main pygame renderer and UI-to-core orchestration loop."""

import time

import pygame

from core.config import load_config
from core.game_state import GameState
from ui.game_over import game_over
from ui.game_view import game_view
from ui.highscores import highscore_view
from ui.input_handler import handle_event
from ui.instructions import instructions
from ui.menu import background, menu, set_screen, title, window_size
from ui.pause_menu import pause_menu
from ui.victory import victory


def run(config_path: str = "config.json") -> int:
    """Run the game UI using the supplied configuration file."""
    pygame.init()
    # prepar pygame to start

    config = load_config(config_path)
    game = GameState(config)

    pygame.display.set_caption("Pac-Man")
    # caption for the window

    screen = pygame.display.set_mode(window_size())
    set_screen(screen)
    # window size and every thing you will see

    fps = 60
    frame_time = 1 / fps
    previous_time = time.perf_counter()

    ui_state = {
        "page": "main",
        "player_name": "",
    }

    running = True

    while running:
        frame_start = time.perf_counter()
        delta_time = frame_start - previous_time
        previous_time = frame_start

        events = pygame.event.get()
        # save every move like mouse click or keyboard click or close window
        for event in events:
            running = handle_event(event, game, ui_state)
            if not running:
                break

        if not running:
            break

        if game.state == "PLAYING":
            game.tick(delta_time)

        if game.state == "MENU":
            if ui_state["page"] == "main":
                background()
                title()
                menu()
            elif ui_state["page"] == "highscores":
                highscore_view(screen, game)
            elif ui_state["page"] == "instructions":
                instructions(screen)

        elif game.state == "PLAYING":
            game_view(screen, game)

        elif game.state == "PAUSED":
            game_view(screen, game)
            pause_menu(screen)

        elif game.state == "GAME_OVER":
            game_over(
                screen,
                game,
                ui_state["player_name"],
            )

        elif game.state == "VICTORY":
            victory(
                screen,
                game,
                ui_state["player_name"],
            )

        pygame.display.flip()
        # update frame so we can see the change on the screen

        elapsed = time.perf_counter() - frame_start
        sleep_time = frame_time - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)
            # for delay so we can work on 60fps

    pygame.quit()
    # quit the pygame we useit after pygame.init()
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
