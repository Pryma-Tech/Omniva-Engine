"""Analysis prompt template."""

from ai.prompt_engine import PromptTemplate

analysis_prompt = PromptTemplate(
    "analysis",
    """
Analyze the video transcript and identify the most viral moments.
Keywords: {{{keywords}}}
Transcript: {{{transcript}}}
Return timestamps and a score.
"""
)
