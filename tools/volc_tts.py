#!/usr/bin/env python3
"""One-request Doubao TTS 2.0 adapter, kept outside the author's Skill."""

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request
import uuid


ENDPOINT = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
DEFAULT_SPEAKER = "zh_female_vv_uranus_bigtts"


def parse_event(line: bytes):
    line = line.strip()
    if not line.startswith(b"data:"):
        return None
    payload = line[5:].strip()
    if payload == b"[DONE]":
        return {"done": True}
    return json.loads(payload)


def collect_stream(lines):
    audio = bytearray()
    sentences = []
    usage = None
    finished = False
    for line in lines:
        event = parse_event(line)
        if event is None:
            continue
        if event.get("done"):
            break
        code = event.get("code")
        if code == 0:
            chunk = event.get("data")
            if chunk:
                audio.extend(base64.b64decode(chunk, validate=True))
            sentence = event.get("sentence")
            if sentence is not None:
                sentences.append(sentence)
        elif code == 20000000:
            # A completion frame can carry final audio or subtitle data too.
            chunk = event.get("data")
            if chunk:
                audio.extend(base64.b64decode(chunk, validate=True))
            sentence = event.get("sentence")
            if sentence is not None:
                sentences.append(sentence)
            usage = event.get("usage")
            finished = True
        else:
            raise ValueError(f"TTS service returned status {code}: {event.get('message', 'unknown error')}")
    if not finished or not audio:
        raise ValueError("TTS response ended without both a completion frame and audio")
    return bytes(audio), sentences, usage


def synthesize(text, speaker, api_key):
    payload = {
        "req_params": {
            "text": text,
            "speaker": speaker,
            "audio_params": {
                "format": "mp3",
                "sample_rate": 24000,
                "bit_rate": 64000,
                "enable_subtitle": True,
            },
        }
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "X-Api-Key": api_key,
            "X-Api-Resource-Id": "seed-tts-2.0",
            "X-Api-Request-Id": str(uuid.uuid4()),
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        return collect_stream(response)


def main():
    parser = argparse.ArgumentParser(description="Generate one MP3 from a finalized script; no automatic retries.")
    parser.add_argument("--text-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--speaker", default=DEFAULT_SPEAKER)
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs without calling the service")
    args = parser.parse_args()

    text = args.text_file.read_text(encoding="utf-8-sig").strip()
    if not text:
        parser.error("The script is empty")
    if len(text) > 1000:
        parser.error("Script exceeds 1000 characters; review and split it manually")
    if args.output.suffix.lower() != ".mp3":
        parser.error("Output must end in .mp3")
    timing_file = args.output.with_suffix(".timing.json")
    if args.output.exists() or timing_file.exists():
        parser.error("Output already exists; choose a new filename")
    print(f"Characters: {len(text)}; resource: seed-tts-2.0; speaker: {args.speaker}")
    if args.dry_run:
        print("Dry run complete; no request sent.")
        return 0

    api_key = os.environ.get("VOLC_TTS_API_KEY")
    if not api_key:
        parser.error("VOLC_TTS_API_KEY is missing from this environment")
    try:
        audio, sentences, usage = synthesize(text, args.speaker, api_key)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temp_file = args.output.with_suffix(".mp3.part")
        try:
            with temp_file.open("xb") as handle:
                handle.write(audio)
            temp_file.replace(args.output)
            timing_file.write_text(
                json.dumps(
                    {
                        "resource_id": "seed-tts-2.0",
                        "speaker": args.speaker,
                        "script_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                        "sentences": sentences,
                        "usage": usage,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
        finally:
            temp_file.unlink(missing_ok=True)
    except urllib.error.HTTPError as exc:
        print(f"TTS HTTP error {exc.code}; check plan, API key, resource and speaker permissions.", file=sys.stderr)
        return 1
    except (urllib.error.URLError, ValueError, json.JSONDecodeError) as exc:
        print(f"TTS request failed: {exc}", file=sys.stderr)
        return 1
    print(f"Saved {args.output} ({len(audio)} bytes) and {timing_file}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

