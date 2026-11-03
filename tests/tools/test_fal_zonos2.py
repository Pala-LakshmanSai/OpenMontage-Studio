"""Offline Zonos2 queue and input contract tests."""
import hashlib
import json
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

from tools.audio.fal_zonos2 import FalZonos2


class ZonosTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        audio = root / 'voice.wav'
        with wave.open(str(audio), 'wb') as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(8000)
            f.writeframes(b'\0\0' * 8000 * 3)
        self.inputs = {'text': 'A short planned line.', 'audio_path': str(audio),
                       'audio_sha256': hashlib.sha256(audio.read_bytes()).hexdigest(),
                       'audio_url': 'https://v3b.fal.media/files/test/voice.wav',
                       'job_path': str(root / 'job.json'), 'output_path': str(root / 'out.wav')}
        self.tool = FalZonos2()
        payload = self.tool.build_request(self.inputs)
        self.inputs['expected_payload_sha256'] = hashlib.sha256(json.dumps(
            payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

    def tearDown(self):
        self.temp.cleanup()

    def test_schema_and_reference_verification(self):
        payload = self.tool.build_request(self.inputs)
        self.assertEqual(payload['language'], 'en_us')
        self.assertEqual(payload['max_tokens'], 1000)
        self.assertTrue(payload['accurate_mode'])
        self.assertEqual(self.tool.estimate_cost(self.inputs), .05)
        changed = dict(self.inputs, audio_sha256='wrong')
        with self.assertRaisesRegex(ValueError, 'hash'):
            self.tool.build_request(changed)
        changed = dict(self.inputs, audio_url='https://example.com/voice.wav')
        with self.assertRaisesRegex(ValueError, 'CDN'):
            self.tool.build_request(changed)

    def test_expressive_mode_is_explicit_boolean_and_changes_payload(self):
        original = self.tool.build_request(self.inputs)
        explicit = self.tool.build_request(dict(self.inputs, accurate_mode=True))
        expressive = self.tool.build_request(dict(self.inputs, accurate_mode=False))
        self.assertEqual(original, explicit)
        self.assertFalse(expressive['accurate_mode'])
        self.assertNotEqual(original, expressive)
        with self.assertRaisesRegex(ValueError, 'boolean'):
            self.tool.build_request(dict(self.inputs, accurate_mode='false'))

    def test_unknown_post_never_replays(self):
        with patch.dict('os.environ', {'FAL_KEY': 'not-a-real-key'}), patch(
                'tools.audio.fal_zonos2.request_json', side_effect=TimeoutError) as req:
            self.assertFalse(self.tool.execute(self.inputs).success)
            self.assertFalse(self.tool.execute(self.inputs).success)
            self.assertEqual(req.call_count, 1)

    def test_accepted_job_resumes_without_post(self):
        accepted = {'request_id': 'fake', 'status_url': 'https://queue.fal.run/s',
                    'response_url': 'https://queue.fal.run/r'}
        with patch.dict('os.environ', {'FAL_KEY': 'not-a-real-key'}), patch(
                'tools.audio.fal_zonos2.request_json', return_value=accepted) as req, patch(
                'tools.audio.fal_zonos2.poll', side_effect=TimeoutError):
            self.assertFalse(self.tool.execute(self.inputs).success)
            self.assertFalse(self.tool.execute(self.inputs).success)
            self.assertEqual(req.call_count, 1)
            self.assertEqual(json.loads(Path(self.inputs['job_path']).read_text())['job']['request_id'], 'fake')

    def test_completed_audio_saves_without_resubmission(self):
        accepted = {'request_id': 'fake', 'status_url': 'https://queue.fal.run/s',
                    'response_url': 'https://queue.fal.run/r'}
        class Response:
            status_code = 200
            def raise_for_status(self): pass
            def iter_content(self, chunk_size):
                yield Path(self_audio_path).read_bytes()
        self_audio_path = self.inputs['audio_path']
        with patch.dict('os.environ', {'FAL_KEY': 'not-a-real-key'}), patch(
                'tools.audio.fal_zonos2.request_json', side_effect=[accepted,
                    {'audio': {'url': 'https://v3b.fal.media/files/test/out.wav'}}]), patch(
                'tools.audio.fal_zonos2.poll'), patch('requests.get', return_value=Response()):
            result = self.tool.execute(self.inputs)
        self.assertTrue(result.success, result.error)
        self.assertTrue(Path(self.inputs['output_path']).is_file())
        self.assertEqual(result.data['request_id'], 'fake')


if __name__ == '__main__':
    unittest.main()
