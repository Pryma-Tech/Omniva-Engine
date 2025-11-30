"""Basic health checks for Omniva Engine.

This module provides lightweight, side-effect-free helpers that are used by
the `/health` HTTP endpoint and internal status probes.
"""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/core/health with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/core/health with cognitive telemetry.

import os

from .job_queue import job_queue


def check_storage() -> dict:
    try:
        os.listdir("storage")
        return {"ok": True}
    except Exception as exc:  # pylint: disable=broad-except
        return {"ok": False, "error": str(exc)}


def check_jobs() -> dict:
    return {
        "queue_length": len(job_queue.queue),
        "total_jobs": len(job_queue.jobs),
    }


def check_uploader() -> dict:
    path = os.path.join("storage", "oauth", "token.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8"):
                return {"ok": True}
        except Exception as exc:  # pylint: disable=broad-except
            return {"ok": False, "error": str(exc)}
    return {"ok": False, "error": "token missing"}
