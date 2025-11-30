"""Shim module so `import app.*` resolves to `backend.app.*`."""

from importlib import import_module
import sys

_backend_app = import_module("backend.app")
sys.modules[__name__] = _backend_app

