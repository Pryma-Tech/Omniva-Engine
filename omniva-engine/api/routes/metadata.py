"""Metadata generation routes."""
# TODO: Secure metadata generation, add persistence.

from fastapi import APIRouter

from metadata.generator import MetadataGenerator
from ai.prompt_engine import prompt_engine

metadata_generator = MetadataGenerator(prompt_engine)
router = APIRouter()


@router.post("/generate")
async def generate_metadata(data: dict) -> dict:
    """Generate metadata for a clip (placeholder)."""
    topic = data.get("topic", "general")
    keywords = data.get("keywords", [])
    return metadata_generator.generate_all(topic, keywords)
