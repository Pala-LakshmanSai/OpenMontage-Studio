import json
import hashlib
import os
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

from tools.audio.fal_audio_review import FalAudioReview


class AudioReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.audio = self.dir / 'audio.wav'
        with wave.open(str(self.audio), 'wb') as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(8000)
            f.writeframes(b'\0\0' * 8000)
        self.inputs = {'audio_path': str(self.audio), 'prompt': 'Review this audio.',
                       'job_path': str(self.dir / 'job.json'), 'output_path': str(self.dir / 'review.json')}
        self.tool = FalAudioReview()
        self.env = patch.dict(os.environ, {'FAL_KEY': 'offline-test-key'})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_schema_controls_and_20_minute_reservation(self):
        fake_probe = json.dumps({'format': {'duration': '1200'}, 'streams': [{'codec_type': 'audio'}]})
        with patch('tools.audio.fal_audio_review.subprocess.check_output', return_value=fake_probe):
            payload, reserve = self.tool.build_request(self.inputs)
        self.assertEqual(str(reserve), '0.30')
        self.assertEqual(payload['max_tokens'], 8192)
        self.assertEqual(payload['model'], 'google/gemini-3.8-flash')
        self.assertFalse(payload['enable_web_search'])
        self.assertIs(payload['reasoning'], True)
        self.assertTrue(payload['audio_url'].startswith('data:audio/wav;base64,'))

    def test_hosted_audio_is_hash_bound_and_extension_checked(self):
        source_hash = hashlib.sha256(self.audio.read_bytes()).hexdigest()
        valid = dict(self.inputs, audio_url='https://v3b.fal.media/files/b/test/review.wav',
                     audio_sha256=source_hash)
        payload, _ = self.tool.build_request(valid)
        self.assertTrue(payload['audio_url'].endswith('/review.wav'))
        for changed in [dict(valid, audio_sha256='bad'),
                        dict(valid, audio_url='https://example.com/review.wav'),
                        dict(valid, audio_url='https://v3b.fal.media/files/b/test/review.bin')]:
            with self.assertRaises(ValueError):
                self.tool.build_request(changed)

    def test_old_receipts_are_preserved_and_never_replayed(self):
        payload, _ = self.tool.build_request(self.inputs)
        del payload['reasoning']
        old_hash = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        receipt_path = Path(self.inputs['job_path'])
        for receipt in (
            {'sha256': old_hash, 'state': 'submitting'},
            {'sha256': old_hash, 'state': 'accepted', 'job': {
                'request_id': 'old', 'status_url': 'https://queue.fal.run/status',
                'response_url': 'https://queue.fal.run/result'}},
        ):
            original = json.dumps(receipt)
            receipt_path.write_text(original)
            with patch('tools.audio.fal_audio_review.request_json') as request:
                self.assertFalse(self.tool.execute(self.inputs).success)
                request.assert_not_called()
            self.assertEqual(receipt_path.read_text(), original)

    def test_ambiguous_post_never_replayed(self):
        with patch('tools.audio.fal_audio_review.request_json', side_effect=TimeoutError) as request:
            self.assertFalse(self.tool.execute(self.inputs).success)
            self.assertFalse(self.tool.execute(self.inputs).success)
            self.assertEqual(request.call_count, 1)
        self.assertEqual(json.loads(Path(self.inputs['job_path']).read_text())['state'], 'submitting')

    def test_resume_known_acceptance_and_changed_input(self):
        submission = {'request_id': 'a', 'status_url': 'https://queue.fal.run/status',
                      'response_url': 'https://queue.fal.run/result'}
        def request(method, url, **kwargs):
            if method == 'POST': return submission
            return {'output': 'AI assessment', 'usage': {'cost': 0.01}}
        with patch('tools.audio.fal_audio_review.request_json', side_effect=request) as calls:
            with patch('tools.audio.fal_audio_review.poll', side_effect=TimeoutError):
                self.assertFalse(self.tool.execute(self.inputs).success)
            changed = dict(self.inputs, prompt='different')
            self.assertFalse(self.tool.execute(changed).success)
            with patch('tools.audio.fal_audio_review.poll'):
                self.assertTrue(self.tool.execute(self.inputs).success)
            self.assertEqual(sum(c.args[0] == 'POST' for c in calls.call_args_list), 1)
        out = json.loads(Path(self.inputs['output_path']).read_text())
        self.assertEqual(out['kind'], 'AI audio assessment, not human listening')

    def test_payload_change_after_reservation_blocks_post(self):
        inputs = dict(self.inputs, expected_payload_sha256='invalid')
        with patch('tools.audio.fal_audio_review.request_json') as request:
            self.assertFalse(self.tool.execute(inputs).success)
            request.assert_not_called()


if __name__ == '__main__':
    unittest.main()
