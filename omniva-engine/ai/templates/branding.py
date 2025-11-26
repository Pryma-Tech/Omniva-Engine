"""Branding prompt template."""

from ai.prompt_engine import PromptTemplate

branding_prompt = PromptTemplate(
    "branding",
    """
Generate branding identity for a YouTube niche channel.
Channel: {{{channel_name}}}
Keywords: {{{keywords}}}
Return: positioning, tone, visual style.
"""
)
