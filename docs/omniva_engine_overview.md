# Omniva Engine — System Overview

## 1. Purpose
Omniva Engine is a hybrid cognitive + operational automation platform that manages autonomous clip-farming workflows end-to-end. It fuses advanced reasoning subsystems (Pantheon, Horizon, Paradox, etc.) with concrete pipeline workers (scraper, analyzer, editor, uploader, scheduler) to orchestrate large-scale short-form content generation without manual intervention.

## 2. System Objectives
- Fully autonomous video-to-clip pipeline
- High reliability via cognitive subsystems (Paradox, Eclipse, Infinity, Zenith)
- Intelligent prioritization through semantic routing and lattice fabrics
- Transparent metadata lineage via the Stardust graph
- Interpretable decision behavior powered by HaloLux
- Long-horizon continuity and purpose alignment through Horizon
- Multi-agent decision refinement with Pantheon archetypes

## 3. High-Level Capabilities
- Multi-platform scraping (TikTok, Instagram Reels, YouTube Shorts)
- AI-driven analysis, transcript generation, and clip scoring
- Automated video editing pipeline (rendering, branding, captioning)
- Auto-uploading plus scheduling optimization for optimal audience windows
- Branding and title/description automation aligned with Chorus/Horizon signals
- Metadata tracking with Stardust to maintain provenance for every clip and decision
- Crisis-mode recovery through Infinity (autoscaling) + Eclipse (failsafe rituals)

## 4. Architectural Overview
```
[Cognitive Layer]
  - Paradox Engine
  - Eclipse Engine
  - Stardust Layer
  - Lattice Router
  - Horizon Engine
  - Pantheon Agents
  - Chorus Harmonizer
  - HaloLux Interpretability
  - Zenith Integrator

↓ Controls / Guides / Monitors ↓

[Operational Layer]
  - Scraper Worker
  - Analyzer Worker
  - Editor Worker
  - Uploader Worker
  - Scheduler Worker
  - Dashboard UI
  - Database + Metadata Store
```

## 5. Cognitive–Operational Interaction
- Paradox continuously checks for conflicting jobs, duplicate timestamps, or drift spikes before operational execution.
- Eclipse coordinates soft rebuilds, subsystem resets, and full reboot rituals after worker or node failures.
- Stardust attaches metadata packets to every pipeline action, preserving lineage for each produced clip.
- Lattice routes priorities and semantic relationships, ensuring downstream workers receive context-aware jobs.
- Horizon tracks project-level goals and long-horizon objectives that bias scheduling and strategy selection.
- Pantheon archetypes vote on clip importance, risk appetite, and exploration preferences before scheduling.
- Chorus harmonizes the emotional tone used for titles, descriptions, and creative assets across workers.
- HaloLux exposes interpretability hooks so operators can inspect reasoning chains for any decision.
- Zenith aggregates messages from cognitive subsystems, computing coherence scores and reflection reports to keep operations aligned.

## 6. Example End-to-End Flow
1. User adds creators and project configuration via the dashboard.
2. Scraper workers download recent videos from TikTok/IG/YouTube.
3. Analyzer workers transcribe footage, run AI scoring, and pass candidate clips to strategy.
4. Pantheon agents evaluate scoring, refining priorities with archetype voting and Chorus modulation.
5. Editor workers render clips with FFmpeg, applying templates, captions, and branding.
6. Uploader workers post finalized clips to YouTube and other platforms.
7. Scheduler optimizes posting times using Oracle forecasts and Horizon goals.
8. Stardust records full provenance for every step, linking packets across the Lattice fabric.
9. HaloLux provides a reasoning chain so operators can review why each clip was produced and scheduled.
