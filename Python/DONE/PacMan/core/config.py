"""Configuration loader module for Pac-Man."""

import json
import copy
import logging
import math
from typing import Any, Dict

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("core.config")

DEFAULT_CONFIG: Dict[str, Any] = {
    "highscore_filename": "highscores.json",
    "level": [
        "level1",
        "level2",
        "level3",
        "level4",
        "level5",
        "level6",
        "level7",
        "level8",
        "level9",
        "level10",
    ],
    "width": 15,
    "height": 15,
    "lives": 3,
    "pacgum": 10,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90.0,
    "enable_42": True,
}


def load_config(filepath: str) -> Dict[str, Any]:
    """Load, parse, and validate the game configuration.

    Ignores full-line comments and unknown JSON keys (including # keys).

    Args:
        filepath (str): The path to the configuration file.

    Returns:
        Dict[str, Any]: The validated configuration dictionary.
    """
    config = copy.deepcopy(DEFAULT_CONFIG)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        clean_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue
            clean_lines.append(line)

        json_str = "".join(clean_lines)
        parsed_data = json.loads(json_str)
        if not isinstance(parsed_data, dict):
            logger.error("Config must be a JSON object. Using defaults.")
            return config

        # Unknown keys (including JSON keys beginning with '#') are ignored.
        # A '#'-prefixed JSON key is data, not an instruction to strip
        # the line; full-line comments are separately supported above.
        for key, default_val in DEFAULT_CONFIG.items():
            if key not in parsed_data:
                logger.warning("Missing key '%s'. Using default.", key)
                continue
            val = parsed_data[key]
            if isinstance(default_val, float):
                if type(val) not in (int, float):
                    logger.warning(
                        "Key '%s' has invalid type. Using default.", key
                    )
                    continue
                try:
                    val = float(val)
                except OverflowError:
                    logger.warning(
                        "Key '%s' is too large. Using default.", key
                    )
                    continue
            if type(val) is type(default_val):
                config[key] = val
            else:
                logger.warning(
                    "Key '%s' has invalid type. Using default.", key
                )

    except FileNotFoundError:
        logger.error("File '%s' not found. Using defaults.", filepath)
    except json.JSONDecodeError as e:
        logger.error("JSON error in '%s': %s. Using defaults.", filepath, e)
    except Exception as e:
        logger.error("Error loading '%s': %s. Using defaults.", filepath, e)

    # Bounds clamping per 42 subject rules (Section 5.3)
    if config["lives"] < 1:
        logger.warning("Config 'lives' must be >= 1. Using default.")
        config["lives"] = DEFAULT_CONFIG["lives"]

    if (
        not math.isfinite(config["level_max_time"])
        or config["level_max_time"] <= 0.0
    ):
        logger.warning(
            "Config 'level_max_time' must be finite and > 0. Using default."
        )
        config["level_max_time"] = DEFAULT_CONFIG["level_max_time"]

    for score_key in (
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        "pacgum",
    ):
        if config[score_key] < 0:
            logger.warning(
                "Config '%s' cannot be negative. Using default.", score_key
            )
            config[score_key] = DEFAULT_CONFIG[score_key]

    for dimension in ("width", "height"):
        if not 5 <= config[dimension] <= 100:
            logger.warning(
                "Config '%s' must be between 5 and 100. Using default.",
                dimension,
            )
            config[dimension] = DEFAULT_CONFIG[dimension]

    if config["seed"] <= 0:
        logger.warning("Config 'seed' must be > 0. Using fixed default.")
        config["seed"] = DEFAULT_CONFIG["seed"]

    filename = config["highscore_filename"]
    if not filename.strip() or "\x00" in filename:
        logger.warning("Invalid highscore filename. Using default.")
        config["highscore_filename"] = DEFAULT_CONFIG["highscore_filename"]

    if (
        not isinstance(config["level"], list)
        or len(config["level"]) < 10
        or not all(
            type(lvl) in (str, int) and str(lvl).strip()
            for lvl in config["level"]
        )
    ):
        logger.warning(
            "Config 'level' must contain at least 10 level names. "
            "Using default level list."
        )
        config["level"] = copy.deepcopy(DEFAULT_CONFIG["level"])
    else:
        config["level"] = [str(lvl) for lvl in config["level"]]

    return config
