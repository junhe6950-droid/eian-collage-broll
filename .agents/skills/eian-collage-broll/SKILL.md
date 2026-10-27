---
name: eian-collage-broll
description: Use the author's original eian-collage-broll paper collage B-roll workflow for finalized narration text. Read the repository root SKILL.md and its references; produce the author's first-frame.png, last-frame.png, and video-prompt.txt deliverables with Gate 1 and Gate 2 approvals.
---

# Repository-local entry point

The author-maintained source of truth is the repository root `SKILL.md`, three parent directories above this file. Read that file and the `references/` files it names, then follow the author's workflow exactly. This entry point exists so Codex can discover the author's root-level Skill without copying or editing it.

The separate `tools/volc_tts.py` prepares narration audio only when the user explicitly requests TTS. It does not change this Skill's gates, image style, or three deliverables. This Skill does not produce a finished video file.

