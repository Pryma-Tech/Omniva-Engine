"""Metadata prompt template."""

from ai.prompt_engine import PromptTemplate

metadata_prompt = PromptTemplate(
    "metadata",
    """
Generate YouTube metadata for a clip.
Topic: {{{topic}}}
Keywords: {{{keywords}}}
Return: title, description, tags.
"""
)
