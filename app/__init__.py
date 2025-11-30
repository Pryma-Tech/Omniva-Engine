"""Shim module so `import app.*` resolves to the legacy backend.

This keeps tests and local tooling stable while we migrate fully to
the v2 backend under `omniva-v2/backend/app`. Once that migration is
complete, this module can be updated to point at the new backend or
removed entirely.
"""

from importlib import import_module
import sys

_backend_app = import_module("backend.app")
sys.modules[__name__] = _backend_app
