import base64
import json
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from volc_tts import collect_stream


def event(data):
    return ("data: " + json.dumps(data) + "\n").encode("utf-8")


class StreamTests(unittest.TestCase):
    def test_audio_subtitle_and_completion(self):
        lines = [
            event({"code": 0, "data": base64.b64encode(b"ID3a").decode(), "sentence": {"words": [{"word": "你", "startTime": 0.1, "endTime": 0.3}]}}),
            event({"code": 20000000, "data": base64.b64encode(b"b").decode(), "usage": {"text_words": 1}}),
            b"data: [DONE]\n",
        ]
        audio, sentences, usage = collect_stream(lines)
        self.assertEqual(audio, b"ID3ab")
        self.assertEqual(sentences[0]["words"][0]["word"], "你")
        self.assertEqual(usage["text_words"], 1)

    def test_incomplete_stream_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "completion frame"):
            collect_stream([event({"code": 0, "data": base64.b64encode(b"ID3").decode()})])

    def test_service_error_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "45000000"):
            collect_stream([event({"code": 45000000, "message": "speaker permission denied"})])


if __name__ == "__main__":
    unittest.main()

