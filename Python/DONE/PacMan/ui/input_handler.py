"""All pygame input handling for the UI layer."""

from typing import Any

import pygame

from core.states import MenuState
from ui.game_over import game_over_input
from ui.highscores import highscore_button
from ui.instructions import instructions_button
from ui.menu import button
from ui.pause_menu import pause_button
from ui.victory import victory_input


def handle_event(
    event: pygame.event.Event,
    game: Any,
    ui_state: dict[str, str],
) -> bool:
    """Relay user input to the core and update UI-only state."""
    if event.type == pygame.QUIT:
        return False

    if game.state == "MENU":
        page = ui_state["page"]

        if page == "main":
            action = button(event)

            if action == "exit":
                return False
            if action == "start":
                ui_state["player_name"] = ""
                game.start_game()
            elif action == "highscores":
                ui_state["page"] = "highscores"
            elif action == "instructions":
                ui_state["page"] = "instructions"

        elif page == "highscores":
            if highscore_button(event) == "back":
                ui_state["page"] = "main"

        elif page == "instructions":
            if instructions_button(event) == "back":
                ui_state["page"] = "main"

        return True

    if game.state == "PLAYING":
        if event.type != pygame.KEYDOWN:
            return True

        if event.key in (pygame.K_UP, pygame.K_w):
            game.set_player_direction("UP")
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            game.set_player_direction("DOWN")
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            game.set_player_direction("LEFT")
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            game.set_player_direction("RIGHT")
        elif event.key in (pygame.K_p, pygame.K_ESCAPE):
            game.pause()
        elif event.key == pygame.K_c:
            # Cheat mode - Toggle Invincibility
            game.toggle_cheat("invincibility")
        elif event.key == pygame.K_n:
            # Cheat mode - Skip current level
            game.toggle_cheat("skip_level")
        elif event.key == pygame.K_f:
            # Cheat mode - Toggle Ghost Freeze
            game.toggle_cheat("freeze_ghosts")

        return True

    if game.state == "PAUSED":
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_p, pygame.K_ESCAPE):
                game.resume()
                return True

        pause_action = pause_button(event)
        if pause_action == "resume":
            game.resume()
        elif pause_action == "menu":
            ui_state["page"] = "main"
            ui_state["player_name"] = ""
            game.change_state(MenuState())

        return True

    if game.state == "GAME_OVER":
        name, submit = game_over_input(
            event,
            ui_state["player_name"],
        )
        ui_state["player_name"] = name
        if submit:
            game.submit_highscore(name)
            ui_state["page"] = "main"
            ui_state["player_name"] = ""
        return True

    if game.state == "VICTORY":
        name, submit = victory_input(
            event,
            ui_state["player_name"],
        )
        ui_state["player_name"] = name
        if submit:
            game.submit_highscore(name)
            ui_state["page"] = "main"
            ui_state["player_name"] = ""
        return True

    return True
