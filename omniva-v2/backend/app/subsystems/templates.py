"""Template subsystem for Omniva Engine v2 (placeholder)."""

from typing import Any, Dict, List

from app.core.registry import registry
from app.models.template import StyleTemplate


class TemplateSubsystem:
    """Placeholder template/style engine."""

    name = "templates"

    def __init__(self) -> None:
        self.templates: List[StyleTemplate] = []

    def initialize(self) -> dict:
        return {"status": "template subsystem initialized (placeholder)"}

    def add_template(self, template: StyleTemplate) -> Dict[str, Any]:
        self.templates.append(template)
        return {"added": template.dict()}

    def list_templates(self) -> List[Dict[str, Any]]:
        return [template.dict() for template in self.templates]

    def get_template(self, name: str) -> Dict[str, Any]:
        for template in self.templates:
            if template.name == name:
                return template.dict()
        return {"error": "template not found (placeholder)"}

    def status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "template_count": len(self.templates),
            "status": "ok (placeholder)",
        }


registry.register_subsystem("templates", TemplateSubsystem())
