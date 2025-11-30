"""Autonomous mode engine for Omniva Engine v2."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/autonomous/autonomous_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/autonomous/autonomous_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/autonomous/autonomous_engine with cognitive telemetry.


import asyncio
from typing import Any, Dict, List

from app.core.registry import registry
from app.core.event_bus import event_bus

from .autonomous_store import AutonomousStore


class AutonomousEngine:
    """Automatically run pipelines according to quotas."""

    name = "autonomous"

    def __init__(self) -> None:
        self.store = AutonomousStore()
        self.running = False
        self._task: asyncio.Task | None = None

    def initialize(self) -> dict:
        return {"status": "autonomous engine initialized"}

    async def run_cycle(self) -> None:
        pm = registry.get_subsystem("project_manager")
        projects = pm.list_projects() if pm else []

        downloader = registry.get_subsystem("downloader")
        transcriber = registry.get_subsystem("transcription")
        analyzer = registry.get_subsystem("analysis")
        editor = registry.get_subsystem("editing")
        uploader = registry.get_subsystem("uploader")

        intel = registry.get_subsystem("intelligence")
        discover = registry.get_subsystem("discovery")

        for project in projects:
            pid = project["id"]
            if not project.get("autonomous", False):
                continue

            # ================
            # 1. DISCOVERY
            # ================
            links = discover.discover_new_posts(pid)
            if not links:
                event_bus.publish("autonomous_no_new_links", {"project_id": pid})
                continue

            event_bus.publish(
                "autonomous_discovered_links",
                {"project_id": pid, "links": links},
            )

            clipCandidates: List[Dict[str, Any]] = []

            for link in links:
                # ================
                # 2. DOWNLOAD
                # ================
                try:
                    local = await downloader.download(pid, link)
                    event_bus.publish(
                        "autonomous_clip_downloaded",
                        {"project_id": pid, "link": link, "local": local},
                    )
                except Exception as e:  # pylint: disable=broad-except
                    event_bus.publish(
                        "autonomous_download_failed",
                        {"project_id": pid, "link": link, "error": str(e)},
                    )
                    continue

                # ================
                # 3. TRANSCRIPTION
                # ================
                try:
                    transcript = await transcriber.transcribe(local)
                    event_bus.publish(
                        "autonomous_transcribed",
                        {"project_id": pid, "file": local, "transcript": transcript},
                    )
                except Exception as e:  # pylint: disable=broad-except
                    event_bus.publish(
                        "autonomous_transcription_failed",
                        {"project_id": pid, "file": local, "error": str(e)},
                    )
                    continue

                # ================
                # 4. ANALYSIS
                # ================
                try:
                    analysis = analyzer.analyze(transcript)
                    event_bus.publish(
                        "autonomous_analyzed",
                        {"project_id": pid, "analysis": analysis},
                    )
                except Exception as e:  # pylint: disable=broad-except
                    event_bus.publish(
                        "autonomous_analysis_failed",
                        {"project_id": pid, "file": local, "error": str(e)},
                    )
                    continue

                # Build clip candidate record
                candidate = {
                    "id": analysis.get("clip_id", link),
                    "transcript": transcript,
                    "meta": {"link": link, "local": local},
                }
                clipCandidates.append(candidate)

            if not clipCandidates:
                event_bus.publish(
                    "autonomous_no_clip_candidates", {"project_id": pid}
                )
                continue

            # ================
            # 5. GENERATE SCORES
            # ================

            # Semantic
            semantic_scores = intel.semantic_rank(pid, clipCandidates)

            # Keywords / Trending
            keyword_scores = intel.keyword_ranker.rank(pid, clipCandidates)

            # Audio scores (stubbed for now)
            audio_scores: List[Dict[str, Any]] = []
            for c in clipCandidates:
                audio_scores.append(
                    {
                        "clip_id": c["id"],
                        # placeholder: audio_score = trending_count or 0
                        "audio_score": intel.audio_trends.match(pid, c["meta"])
                        .get("recommendations", [{}])[0]
                        .get("count", 0),
                    }
                )

            event_bus.publish(
                "autonomous_scores_generated",
                {
                    "project_id": pid,
                    "semantic": semantic_scores,
                    "keyword": keyword_scores,
                    "audio": audio_scores,
                },
            )

            # ================
            # 6. PRIORITIZATION (Step 56)
            # ================
            priority = intel.prioritize_with_personality(
                pid, semantic_scores, keyword_scores, audio_scores
            )

            event_bus.publish(
                "autonomous_prioritized",
                {"project_id": pid, "priority": priority},
            )

            # ================
            # 7. RECOMMENDATION ENGINE (Step 57)
            # ================
            recommendations = intel.recommend_clips(
                pid, priority, limit=project.get("daily_limit", 3)
            )

            event_bus.publish(
                "autonomous_recommended",
                {"project_id": pid, "recommendations": recommendations},
            )

            # ================
            # 8. DECIDE UPLOAD OR SCHEDULE
            # ================

            # User preference:
            mode = project.get("auto_publish_mode", "schedule")
            # options:
            #   - schedule (default)
            #   - instant
            #   - mixed (future)

            for rec in recommendations:
                clip_id = rec["clip_id"]

                # Find candidate file
                candidate = next(
                    (c for c in clipCandidates if c["id"] == clip_id), None
                )
                if not candidate:
                    continue

                local_file = candidate["meta"]["local"]

                # ================
                # 8A. EDIT VIDEO
                # ================
                try:
                    rendered = await editor.render(
                        pid, local_file, candidate["transcript"]
                    )
                except Exception as e:  # pylint: disable=broad-except
                    event_bus.publish(
                        "autonomous_edit_failed",
                        {"project_id": pid, "clip_id": clip_id, "error": str(e)},
                    )
                    continue

                # ================
                # 8B. PUBLISH OR SCHEDULE
                # ================
                if mode == "instant":
                    try:
                        result = await uploader.upload(pid, rendered)
                        event_bus.publish(
                            "autonomous_uploaded",
                            {
                                "project_id": pid,
                                "clip_id": clip_id,
                                "youtube": result,
                            },
                        )
                    except Exception as e:  # pylint: disable=broad-except
                        event_bus.publish(
                            "autonomous_upload_failed",
                            {"project_id": pid, "clip_id": clip_id, "error": str(e)},
                        )
                else:
                    # schedule mode (default)
                    scheduler = registry.get_subsystem("scheduler")
                    try:
                        scheduler.queue_clip(pid, rendered, rec["explanation"])
                        event_bus.publish(
                            "autonomous_scheduled",
                            {
                                "project_id": pid,
                                "clip_id": clip_id,
                                "file": rendered,
                                "reason": rec["explanation"],
                            },
                        )
                    except Exception as e:  # pylint: disable=broad-except
                        event_bus.publish(
                            "autonomous_schedule_failed",
                            {"project_id": pid, "clip_id": clip_id, "error": str(e)},
                        )

    async def auto_loop(self) -> None:
        """Repeatedly run the autonomous cycle."""
        self.running = True
        while self.running:
            await self.run_cycle()
            await asyncio.sleep(60)

    def start(self) -> None:
        if self._task and not self._task.done():
            return
        self._task = asyncio.create_task(self.auto_loop())

    def stop(self) -> None:
        self.running = False
        if self._task:
            self._task.cancel()
            self._task = None
