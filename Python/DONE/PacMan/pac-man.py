"""Main entry point for the Pac-Man game.

This file validates command-line arguments and starts Adel's renderer,
which owns the game loop and initializes Mustafa's backend engine. Startup
and runtime exceptions are reported without a traceback.
"""

import sys
import logging
from importlib import import_module

# Setup strict logging per 42 requirements
logging.basicConfig(
    level=logging.INFO, format="%(levelname)s [%(name)s]: %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> int:
    """Execute the main entry point combining CLI validation and UI loop.

    Validates that a configuration JSON file was provided, orchestrates the
    engine lifecycle, and handles exceptions cleanly without dumping a
    traceback.

    Returns:
        int: Process exit code (0 for success, non-zero for error).
    """
    if len(sys.argv) != 2:
        logger.error("Usage: python3 pac-man.py <config.json>")
        return 1

    config_path = sys.argv[1]
    if not config_path.lower().endswith(".json"):
        logger.error(
            "Invalid configuration file '%s'. Expected a JSON file.",
            config_path,
        )
        return 1

    try:
        logger.info("Initializing Pac-Man Engine...")
        # Delay UI imports until after CLI validation. A missing graphical
        # dependency is an installation error, not a successful game launch.
        renderer = import_module("ui.renderer")
        result: object = renderer.run(config_path)
        if isinstance(result, int):
            return result
        logger.error("The renderer did not return an integer exit status.")
        return 1

    except KeyboardInterrupt:
        logger.info("Game interrupted by user. Exiting cleanly.")
        return 0
    except Exception as err:
        logger.error("Fatal error during execution: %s", err)
        return 1


if __name__ == "__main__":
    sys.exit(main())
