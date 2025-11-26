"""PromptEngine centralizes all prompt generation."""
# TODO: Integrate actual LLM inference (OpenAI, Gemini, etc.)

from utils.logger import logger


class PromptTemplate:
    """Lightweight template helper."""

    def __init__(self, name: str, template: str) -> None:
        self.name = name
        self.template = template

    def render(self, **kwargs) -> str:
        """Render a simple template (placeholder)."""
        text = self.template
        for key, value in kwargs.items():
            text = text.replace(f"{{{{{key}}}}}", str(value))
        return text


class PromptEngine:
    """Registry for prompt templates."""

    def __init__(self) -> None:
        logger.info("PromptEngine initialized (placeholder).")
        self.templates = {}

    def register(self, prompt: PromptTemplate) -> None:
        """Register a prompt template."""
        self.templates[prompt.name] = prompt

    def get(self, name: str):
        """Return a prompt template by name."""
        return self.templates.get(name)

    def render(self, name: str, **kwargs) -> str:
        """Render a prompt by name."""
        tmpl = self.get(name)
        if not tmpl:
            return f"Prompt '{name}' not found."
        return tmpl.render(**kwargs)
