# EIAN collage B-roll + Volc TTS 2.0

- This fork is a separate workflow from all `sweety-handdraw-video` and `guofeng-video-pipeline` chats, repositories, and cloud environments. Do not load, modify, or sync those projects while working here.
- The author's original workflow is defined by root `SKILL.md` and `references/`. Keep those files unchanged. Use the repo-local entry point at `.agents/skills/eian-collage-broll/SKILL.md` to discover and follow the original Skill.
- Use `tools/volc_tts.py` only for an explicitly requested, finalized narration script. It sends one request to Doubao TTS 2.0, does not auto-retry, and does not rewrite the text. Always run `--dry-run` first and report character count and speaker before a billable request.
- Read `VOLC_TTS_API_KEY` from the new cloud environment's scoped network secret. Never print, copy, commit, or paste the value into chat. Allow only `openspeech.bytedance.com` for this API.
- Keep generated audio, timing data, and images in a task-specific directory outside this Git repository, such as `/workspace/eian-collage-jobs/<task-id>/`; never add them to a Git commit without a separate user request.
- The author's Skill produces `first-frame.png`, `last-frame.png`, and `video-prompt.txt`. It does not render or mix a finished voiced MP4. Explain this boundary if the user requests a final video.

