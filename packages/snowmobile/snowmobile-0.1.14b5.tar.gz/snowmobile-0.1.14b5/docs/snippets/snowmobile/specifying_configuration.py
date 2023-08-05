"""
Demonstrate specifying an alternate snowmobile.toml file *path*.
../docs/snippets/snowmobile/specifying_configuration.py
"""
import snowmobile
from pathlib import Path

path = Path.cwd() / 'snowmobile_v2.toml'  # any alternate file path

sn = snowmobile.connect(from_config=path)
# snowmobile-include
