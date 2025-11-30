"""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/templates/template_store.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/templates/template_store with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/templates/template_store with cognitive telemetry.

Filesystem-backed template store.
"""

import json
import os
from typing import Any, Dict, List, Optional

from app.models.template import StyleTemplate


class TemplateStore:
    """Save and load templates from storage/templates/."""

    def __init__(self) -> None:
        self.base = os.path.join("storage", "templates")
        os.makedirs(self.base, exist_ok=True)

    def list_templates(self) -> List[Dict[str, Any]]:
        templates: List[Dict[str, Any]] = []
        for file_name in os.listdir(self.base):
            if not file_name.endswith(".json"):
                continue
            path = os.path.join(self.base, file_name)
            with open(path, "r", encoding="utf-8") as template_file:
                templates.append(StyleTemplate(**json.load(template_file)).dict())
        return templates

    def save_template(self, template: StyleTemplate) -> Dict[str, Any]:
        path = os.path.join(self.base, f"{template.name}.json")
        with open(path, "w", encoding="utf-8") as template_file:
            json.dump(template.dict(), template_file, indent=2)
        return template.dict()

    def load_template(self, name: str) -> Optional[StyleTemplate]:
        path = os.path.join(self.base, f"{name}.json")
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as template_file:
            return StyleTemplate(**json.load(template_file))
