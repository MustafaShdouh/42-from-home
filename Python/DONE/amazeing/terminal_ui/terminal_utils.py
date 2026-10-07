import sys
import os
import select
import termios
import tty
import shutil

_old_termios_settings = None


def setup_terminal() -> None:
    """configures the terminal for raw, non-blocking input without echo."""
    global _old_termios_settings
    fd = sys.stdin.fileno()
    _old_termios_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    # explicitly turn off ECHO
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSADRAIN, new)


def restore_terminal() -> None:
    """restores the terminal to its original state."""
    if _old_termios_settings is not None:
        termios.tcsetattr(
            sys.stdin.fileno(), termios.TCSADRAIN, _old_termios_settings
        )


def check_terminal_size(
    required_cols: int, required_lines: int
) -> tuple[bool, int, int]:
    """checks if the terminal is large enough using shutil."""
    size = shutil.get_terminal_size()
    return (
        (size.columns >= required_cols and size.lines >= required_lines),
        size.columns,
        size.lines,
    )


def clear_screen() -> None:
    """clears the terminal screen."""
    os.system("clear")


def kbhit() -> bool:
    """checks if a keyboard key has been pressed without blocking."""
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    return dr != []


def get_char() -> str:
    """reads a single character from standard input instantly."""
    return sys.stdin.read(1).lower()


def flush_input() -> None:
    """clears any unprocessed keystrokes from the input buffer."""
    try:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except Exception:
        while kbhit():
            sys.stdin.read(1)
