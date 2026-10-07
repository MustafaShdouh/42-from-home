from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    ValidationError,
    ValidationInfo,
)
from typing import Tuple


class MazeConfig(BaseModel):
    """configuration model for the A-Maze-ing project.

    uses Pydantic to validate and store the maze settings parsed from
    the configuration file.

    attributes:
        WIDTH (int): the width of the maze. Minimum 9 to fit the 42 pattern.
        HEIGHT (int): the height of the maze. Minimum 7 to fit the 42 pattern.
        ENTRY (Tuple[int, int]): the starting coordinate of the maze (x, y).
        EXIT (Tuple[int, int]): the ending coordinate of the maze (x, y).
        OUTPUT_FILE (str): the filename where the generated maze is saved.
        PERFECT (bool): true for a perfect maze,
        False for an imperfect maze (Pac-Man style).
        SEED (int | None): the seeding to generate an
        identical maze every make run.
    """

    model_config = ConfigDict(extra="forbid")

    WIDTH: int = Field(ge=9, description="maze width (min 9)")
    HEIGHT: int = Field(ge=7, description="maze height (min 7)")
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int | None = Field(
        default=None, description="optional seed for reproducibility"
    )

    @field_validator("ENTRY", "EXIT", mode="before")
    @classmethod
    def parse_coordinates(cls, v: str | Tuple[int, int]) -> Tuple[int, int]:
        """parses the coordinate strings into tuple of ints.

        args:
            v (str | Tuple[int, int]): the string value like "0,0"
            or already parsed tuple.

        returns:
            Tuple[int, int]: the parsed coordinates.

        raises:
            ValueError: if the format is not exactly X,Y
        """
        # we check if it's a string, then we split it by comma and
        # strip whitespaces
        if isinstance(v, str):
            try:
                x_str, y_str = v.split(",")
                return (int(x_str.strip()), int(y_str.strip()))
            except ValueError:
                raise ValueError("Must be in the format X,Y")
        return v

    @field_validator("PERFECT", mode="before")
    @classmethod
    def parse_boolean(cls, v: str | bool) -> bool:
        """parses string booleans gracefully.

        args:
            v (str | bool): the string like "True" or "False".

        returns:
            bool: the actual python boolean value.

        raises:
            ValueError: if it doesn't match 'True' or 'False'.
        """
        # title or lower doesn't matter, just making sure
        # "true" or "True" works
        if isinstance(v, str):
            val = v.strip().lower()
            if val == "true":
                return True
            elif val == "false":
                return False
            raise ValueError("Must be 'True' or 'False'")
        return v

    @field_validator("EXIT")
    @classmethod
    def check_entry_exit_different(
        cls, v: Tuple[int, int], info: ValidationInfo
    ) -> Tuple[int, int]:
        """ensures that the entry and exit are not the same coordinate."""
        # we cant have the start and end be the exact same spot
        if "ENTRY" in info.data and v == info.data["ENTRY"]:
            raise ValueError("ENTRY and EXIT must be different cells.")
        return v


def config_parser(filepath: str = "config.txt") -> MazeConfig | None:
    """parses the config.txt file and validates using Pydantic.

    reads the file line by line, ignores comments, strips spaces,
    and then feeds it to our MazeConfig model for validation.

    args:
        filepath (str): path to the config text file. Defaults to "config.txt".

    returns:
        MazeConfig | None: the validated config object,
        or None if errors occurred.
    """
    from typing import Any

    # the dictionary to store the values in the config file
    values: dict[str, Any] = {}
    try:
        # parsing the config file line by line
        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                # if the line starts with a #
                # we skip it and consider it a comment
                if not line or line.startswith("#"):
                    continue
                # we do this in case the = sign is a part of
                # the name or value of the config value,
                # if it is then we just take the first =
                if "=" not in line:
                    raise ValueError(
                        f"Invalid configuration syntax in line: {line}"
                    )

                # here we are just tuple unpacking the items before
                # the = and after into key and value
                key, val = line.split("=", 1)

                # just some cleaning up and using upper
                # to make sure that we dont have duplicates
                key = key.strip().upper()
                if key in values:
                    raise ValueError(f"Duplicated config item: {key}")
                values[key] = val.strip()

        # validate through Pydantic (this does all the heavy lifting for types)
        config = MazeConfig(**values)

        # additional bounds check for entry and exit against width/height
        if not (
            0 <= config.ENTRY[0] < config.WIDTH
            and 0 <= config.ENTRY[1] < config.HEIGHT
        ):
            raise ValueError(
                f"ENTRY {config.ENTRY} is out of bounds for maze "
                f"{config.WIDTH}x{config.HEIGHT}."
            )
        if not (
            0 <= config.EXIT[0] < config.WIDTH
            and 0 <= config.EXIT[1] < config.HEIGHT
        ):
            raise ValueError(
                f"EXIT {config.EXIT} is out of bounds for maze "
                f"{config.WIDTH}x{config.HEIGHT}."
            )

        return config

    except FileNotFoundError:
        print(f"Error: The configuration file '{filepath}' was not found.")
    except ValidationError as e:
        print("Maze generation aborted due to configuration errors:")
        for err in e.errors():
            print(f" - {err['loc'][0]}: {err['msg']}")
    except Exception as e:
        print(f"Error: {e}")

    return None
