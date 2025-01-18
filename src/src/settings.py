import os
from datetime import timedelta
from pathlib import Path

from split_settings.tools import include


include(
    "components/base.py",
    "components/*.py",
)
