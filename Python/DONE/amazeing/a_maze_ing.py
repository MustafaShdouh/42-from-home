import sys

try:
    from config_parser.parser import config_parser
    from maze_generator import MazeGenerator
    from terminal_ui import interactive_loop

    _MODULES_LOADED = True
except ModuleNotFoundError as e:
    print(f"Error: Missing required module - {e.name}")
    print(
        "If this is an external dependency, try running: pip install <module>"
    )
    _MODULES_LOADED = False


def main() -> None:
    """main entry point for A-Maze-ing.

    parses configuration, generates the maze based on those parameters,
    and writes the final hexadecimal output to the file.
    """
    if not _MODULES_LOADED:
        return

    # if the user passed more than one argument then use
    # the argument they passed, else just use the default config.txt file
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.txt"
    config = config_parser(config_file)

    if not config:
        return

    try:
        # instantiate generator using our config
        generator = MazeGenerator(
            width=config.WIDTH,
            height=config.HEIGHT,
            entry=config.ENTRY,
            exit_coords=config.EXIT,
            perfect=config.PERFECT,
            seed=config.SEED,
        )

        # generate maze structure
        generator.generate()

        # write output file in the hex format requested
        generator.write_output(config.OUTPUT_FILE)
        print(f"Maze successfully generated and saved to {config.OUTPUT_FILE}")

        # start interactive rendering
        interactive_loop(generator)

    except ValueError as e:
        print(f"Error during maze generation: {e}")
        return
    except OSError as e:
        print(
            f"Error: Could not write output file"
            f"'{config.OUTPUT_FILE}' ({e.strerror})."
        )
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return


if __name__ == "__main__":
    main()
