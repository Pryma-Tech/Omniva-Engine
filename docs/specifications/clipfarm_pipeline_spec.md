# Omniva Engine — Clipfarm Pipeline Specification

## 1. Overview
The clipfarm pipeline is the operational backbone of Omniva. It autonomously converts long-form creator videos into optimized short-form clips by linking workers, shared infrastructure, and the Omniva cognitive layer. The cognitive subsystems prioritize sources, validate quality, and enforce strategy, while the pipeline executes scrape → analyze → edit → upload → schedule without manual touch points.

## 2. Pipeline Stages

### 2.1 Scraping & Ingestion
- **Supported platforms**: TikTok, Instagram Reels, YouTube Shorts (extensible via platform adapters).
- **Behavior**:
  - TikTok: Pulls creator feed via private API wrapper, respecting rate limits.
  - Instagram Reels: Uses authenticated session with paging markers.
  - YouTube Shorts: Fetches channel feed or playlist, downloading shorts under 90 seconds.
- **Download rules**: Default window is past 7 days per creator; configurable overrides let Zenith widen or narrow the window based on Horizon strategy.
- **Duplicate detection**: Each media file is hashed (SHA-256). Existing checksums in `videos.checksum` prevent re-downloading; Paradox uses these hashes to flag duplicates across creators.
- **Metadata extraction**: Captions, posted_at timestamps, platform IDs, engagement counters, and hashtags stored in `posts.raw_metadata`.

### 2.2 Analysis Pipeline

#### 2.2.1 Transcript Extraction
- Whisper or cloud ASR options selected per worker pool.
- Supports multi-language detection; language tags stored next to transcripts.
- Confidence scores provided per segment; low-confidence regions trigger reprocessing or manual review flags.

#### 2.2.2 Keyword Detection
- Combines user-defined keyword lists with auto-extracted semantic tags (spaCy/BERT).
- Topic clustering groups clips by theme for Horizon-level diversity metrics.

#### 2.2.3 Virality Scoring
- **Inputs**: Engagement signals (likes/comments/views), velocity metrics (growth rate since posting), NLP sentiment, audience resonance indicators (match to target personas).
- **Outputs**: `virality_score` (0–1) and `relevance_score` (0–1). Stored in `analysis` and fed to Lattice for prioritization.

#### 2.2.4 Clip Candidate Extraction
- Sliding-window scan (5–120 seconds configurable) with stride tuned per platform.
- Silence removal ensures clips start/end on speech or action.
- Speaker change detection (diarization) prevents mid-sentence cuts.
- Action/facial prominence detection verifies subject is centered and expressive.
- Stored fields: `start_time`, `end_time`, `confidence`, `semantic_tags`, plus `pantheon_votes` after scoring.

### 2.3 Cognitive Layer Integration
- **Paradox**: Cross-checks clip/post metadata for duplicates or circular references before jobs progress.
- **Pantheon**: Votes on candidate quality, assigning consensus/confidence that drive which clips move to editing.
- **Lattice**: Assigns processing priority across creators and stages, ensuring GPU/CPU capacity targets the highest strategic value.
- **Horizon**: Adjusts quotas and scheduling weights so the pipeline maintains long-horizon campaign mix (e.g., themes per week).
- **Zenith**: Consumes all signals and issues binding commands (ScraperJob → EditJob → UploadJob → ScheduleTask) to workers.
- **HaloLux/Stardust**: Capture reasoning and provenance at each stage, enabling dashboard traceability.

### 2.4 Editing Pipeline
Automated V1 editing produces publish-ready clips with minimal human touch.

#### 2.4.1 Smart Autocut
- Removes silence using RMS thresholds.
- Trims filler words (“uh”, “like”) via transcript alignment.
- Tightens pacing with beat detection heuristics; minimum jump cut spacing enforced.

#### 2.4.2 Reframing / Cropping
- Enforces 9:16 output; fallback to 1:1 if subject framing fails.
- Face detection + subject tracking keep presenter centered; uses optical flow for continuity.
- Optional Ken Burns-style motion adds energy to static shots.

#### 2.4.3 Audio Processing
- LUFS normalization (-14 target).
- Broadband noise reduction + de-ess filters.
- Light compression (2:1) to smooth dynamics; limiter prevents clipping.

#### 2.4.4 Rendering
- FFmpeg pipelines defined in `EditJob.ffmpeg_commands`.
- GPU acceleration (NVENC) triggered when `gpu_required=true`.
- Output consistency: 1080x1920, 30/60fps as per platform, H.264 video + AAC audio, max 60 MB file size. Checksums stored for dedupe.

### 2.5 Upload Pipeline

#### 2.5.1 Metadata Generation
- AI proposes titles/descriptions using Chorus signals + Pantheon rationale.
- Keywords derived from analysis tags plus platform trend seeds.
- Thumbnail v1 = best-frame screenshot (subject in focus, high brightness). Metadata embedded in `UploadJob`.

#### 2.5.2 YouTube Integration
- OAuth2 per brand account; tokens rotated via secret manager.
- Upload via YouTube Data API videos.insert endpoint; resumable uploads for >50 MB.
- Privacy settings: `public|unlisted|private` set from UploadJob.
- Error handling: quota exhaustion triggers delayed retry; policy violations escalate to Paradox/Eclipse for manual review.

### 2.6 Scheduling Pipeline
- Posting time optimization blends historical engagement, Horizon adjustments, and current queue saturation.
- Daily clip quota ensures creators do not flood feeds (default 5/day configurable).
- Conflict avoidance ensures no double-booking per channel/time slot; Scheduler coordinates with Zenith.
- Horizon-provided long-horizon weights enforce content mix (e.g., 40% educational, 60% entertainment) across the calendar.

## 3. Data Structures Used in the Pipeline
Representative payloads (see full schemas in module interface document):

```jsonc
// ScraperJob
{
  "job_id": "uuid",
  "creator_id": "uuid",
  "platform": "tiktok",
  "target_url": "https://tiktok.com/@creator",
  "requested_range": { "since": "2024-05-01T00:00:00Z", "until": "2024-05-07T00:00:00Z" }
}

// AnalysisResult
{
  "video_id": "uuid",
  "transcript": "...",
  "keywords_detected": ["motivation", "fitness"],
  "virality_score": 0.83,
  "relevance_score": 0.77,
  "clip_candidates": ["clip-uuid-1", "clip-uuid-2"]
}

// ClipCandidate
{
  "clip_id": "uuid",
  "video_id": "uuid",
  "start_time": 45.2,
  "end_time": 72.1,
  "confidence": 0.92,
  "semantic_tags": ["guest_quote", "call_to_action"]
}

// EditJob
{
  "edit_job_id": "uuid",
  "clip_id": "uuid",
  "operations": ["autocut", "reframe", "captions"],
  "ffmpeg_commands": ["ffmpeg -i ..."],
  "gpu_required": true
}

// UploadJob
{
  "upload_job_id": "uuid",
  "clip_id": "uuid",
  "title": "5-Second Productivity Reset",
  "description": "...",
  "keywords": ["productivity", "routine"],
  "scheduled_time": "2024-05-10T16:00:00Z"
}

// ScheduleTask
{
  "schedule_id": "uuid",
  "clip_id": "uuid",
  "recommended_time": "2024-05-12T18:00:00Z",
  "final_decision_source": "zenith"
}
```

## 4. Error Handling
- **Scraper failures**: network retries with exponential backoff; rate-limit responses cause cooldown before reattempt. Invalid URLs routed to Paradox for validation, logged via Stardust.
- **Analysis failures**: ASR timeout triggers secondary ASR provider; malformed video escalates to Scraper for re-download. Analyzer marks job `ERROR` and notifies Eclipse.
- **Editor failures**: FFmpeg crash records command and stderr; Eclipse either retries on same host (max 3) or moves job to GPU-safe pool. Persistent failures quarantine the clip.
- **Upload failures**: Quota exceeded results in automatic defer to next quota window; policy errors require operator review flagged through Dashboard and HaloLux.
- **Scheduler deadlocks**: When overlapping constraints cannot be satisfied, Scheduler emits `scheduler_fault`, prompting Horizon to adjust targets and Zenith to break ties.
- **Eclipse handling**: Central crisis loop classifies failure severity, issues retry/rollback plans, isolates failing workers, and keeps HaloLux updated for operator visibility.

## 5. Performance Considerations
- Parallel scraping via worker pools per platform; concurrency tuned to API limits.
- Batch processing: Analyzer groups videos to reuse model warm starts; Editor batches renders when GPU memory allows.
- Worker scaling: Horizontal auto-scaling on CPU/GPU pools based on queue length and Lattice priority backlog.
- Disk I/O: Local NVMe cache for hot assets, periodic flush to cloud storage; checksums verify integrity post-transfer.
- GPU usage: Reserved for editing and high-throughput ASR; scheduler ensures GPU queues don’t starve CPU-only tasks.
- Queue backpressure: Zenith enforces max in-flight jobs per stage; when thresholds exceeded, upstream stages slow or pause until downstream drains.

## 6. Example End-to-End Execution
1. **Scraper** downloads 12 videos across three creators (past 7 days), storing media + metadata, logging every action to Stardust.
2. **Analyzer** produces transcripts and extracts 38 clip candidates with virality scores; low-confidence transcripts are reprocessed automatically.
3. **Pantheon** ranks candidates, elevating the top 5 with multi-agent consensus >0.8; Lattice adjusts queue priorities accordingly.
4. **Editor** renders the 5 clips using smart autocut + reframing; two require GPU acceleration with NVENC.
5. **Uploader** posts 2 clips immediately (based on Zenith instruction) and schedules the remaining 3 using Scheduler recommendations.
6. **Stardust** links every step, so HaloLux can show source video → clip → edit → upload → schedule lineage on the Dashboard.

## 7. Future Extensions (Pipeline v2+)
- Auto-subtitles with stylized captions and animated karaoke effects.
- Background music recommendation + loudness-aware mixing.
- B-roll injection leveraging stock/video libraries and semantic matching.
- AI voiceovers for narration or dubbing into additional languages.
- Style templates (brand kits) controlling fonts, overlays, motion graphics.
- Multi-clip compound editing to stitch thematic narratives.
- Trend analysis that adapts scraping focus based on real-time social signals.
- Thumbnail generator v2 using Stable Diffusion or similar generative models.
