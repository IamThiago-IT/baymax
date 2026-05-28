from __future__ import annotations

from pathlib import Path

_package_dir = Path(__file__).resolve().parent
_source_package_dir = _package_dir.parent / "src" / "baymax"

__path__ = [str(_package_dir), str(_source_package_dir)]
