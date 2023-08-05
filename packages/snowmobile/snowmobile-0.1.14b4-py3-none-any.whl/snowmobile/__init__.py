"""
A wrapper library around the snowflake-connector-python for streamlined
interaction with the Snowflake database.
"""
# isort: skip_file
# fmt: off
__version__ = "0.1.14b4"
__author__ = "Grant Murray"
__application__ = "snowmobile"

__all__ = [
    # meta
    "__version__",
    "__author__",
    "__application__",

    # API
    "Snowmobile", "connect",
    "SQL",
    "Table",
    "Configuration",
    "Script",
    "Statement",
    "export_config",
]

from .core import (
    SQL,
    Configuration,
    Snowmobile, connect,
    Table,
    Script,
    Section,
    Statement,
    utils,
)

from pathlib import Path
from typing import Optional, Union


def export_config(target_dir: Optional[Union[str, Path]] = None):
    """Exports template `snowmobile.toml` file."""
    return Configuration(export_dir=(target_dir or Path.cwd()))
