"""Editing prompt template."""

from ai.prompt_engine import PromptTemplate

editing_prompt = PromptTemplate(
    "editing",
    """
Generate editing instructions for a short-form viral clip.
Clip start: {{{start}}}
Clip end: {{{end}}}
Style: {{{style}}}
Return steps for zoom, crop, subtitles, and pacing.
"""
)
