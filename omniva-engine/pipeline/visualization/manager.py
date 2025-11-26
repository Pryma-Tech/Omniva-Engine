"""Pipeline Visualization Manager (Placeholder)."""
# TODO: Replace with dynamic step introspection and live status.

from utils.logger import logger


class PipelineVisualizationManager:
    """Return static pipeline graph data."""

    def __init__(self):
        logger.info("PipelineVisualizationManager initialized (placeholder).")

    def get_structure(self) -> dict:
        return {
            "name": "Omniva Clip Pipeline",
            "nodes": [
                {"id": "scrape", "label": "Scrape"},
                {"id": "analyze", "label": "Analyze"},
                {"id": "edit", "label": "Edit"},
                {"id": "metadata", "label": "Metadata"},
                {"id": "upload", "label": "Upload"},
            ],
            "edges": [
                {"from": "scrape", "to": "analyze"},
                {"from": "analyze", "to": "edit"},
                {"from": "edit", "to": "metadata"},
                {"from": "metadata", "to": "upload"},
            ],
        }
