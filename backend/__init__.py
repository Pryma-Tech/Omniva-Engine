"""Backend package bootstrap ensuring `app.*` imports resolve."""

from importlib import import_module
import sys

_app_module = import_module(".app", __name__)
sys.modules.setdefault("app", _app_module)

__all__ = ["_app_module"]

