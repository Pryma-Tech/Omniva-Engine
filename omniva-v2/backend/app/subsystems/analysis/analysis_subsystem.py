"""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/analysis/analysis_subsystem.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/analysis/analysis_subsystem with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/analysis/analysis_subsystem with cognitive telemetry.

Real analysis subsystem performing semantic scoring on transcripts.
"""

import hashlib
import json
import os
from typing import Any, Dict, List, Optional

from app.core.event_bus import event_bus
from app.core.job_queue import job_queue
from app.core.registry import registry
from app.models.analysis import ClipCandidate

from .embedding_engine import EmbeddingEngine
from .silence_detector import detect_silence


class AnalysisSubsystem:
    """Generate clip candidates from normalized transcripts."""

    name = "analysis"

    def __init__(self) -> None:
        self.embedder = EmbeddingEngine()

    def initialize(self) -> Dict[str, str]:
        return {"status": "analysis subsystem initialized"}

    def analyze(self, transcript: str) -> Dict[str, Any]:
        """
        Lightweight analyzer used by the autonomous loop.
        """
        clip_id = hashlib.sha256(transcript.encode("utf-8")).hexdigest()[:12] if transcript else "unknown"
        return {"clip_id": clip_id, "transcript": transcript}

    def analyze_transcript(
        self,
        filepath: str,
        project_id: int,
        keywords: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Core transcript analysis routine."""
        if not os.path.exists(filepath):
            return {"error": "transcript not found", "filepath": filepath}

        with open(filepath, "r", encoding="utf-8") as transcript_file:
            segments: List[Dict[str, Any]] = json.load(transcript_file)

        silence_mask = detect_silence(segments)
        scores = self.embedder.score_segments(segments, keywords or [])

        candidates: List[Dict[str, Any]] = []
        for segment, score, silent in zip(segments, scores, silence_mask):
            if silent:
                continue
            candidate = ClipCandidate(
                start=float(segment.get("start", 0.0)),
                end=float(segment.get("end", 0.0)),
                text=segment.get("text", ""),
                score=float(score),
                keywords=[
                    keyword
                    for keyword in (keywords or [])
                    if keyword.lower() in segment.get("text", "").lower()
                ],
            )
            candidates.append(candidate.dict())

        candidates.sort(key=lambda item: item["score"], reverse=True)

        out_dir = os.path.join("storage", "projects", str(project_id), "analysis")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, os.path.basename(filepath))
        with open(out_path, "w", encoding="utf-8") as analysis_file:
            json.dump(candidates, analysis_file, indent=2)

        result = {
            "project_id": project_id,
            "transcript_filepath": filepath,
            "analysis_filepath": out_path,
            "candidates": candidates,
        }

        event_bus.publish("analysis_complete", result)
        job_queue.enqueue(
            "edit_clip",
            {
                "project_id": project_id,
                "analysis_filepath": out_path,
            },
        )
        return result

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}


registry.register_subsystem("analysis", AnalysisSubsystem())
