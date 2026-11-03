"""Use the editable configuration beside the packaged executable."""

import sys
from pathlib import Path

if len(sys.argv) == 1:
    if getattr(sys, "frozen", False):
        config_path = Path(sys.executable).resolve().parent / "config.json"
        sys.argv.append(str(config_path))
