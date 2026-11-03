"""Offline Qwen3 clone/speech contract and queue safety tests."""
import hashlib, json, tempfile, unittest, wave
from pathlib import Path
from unittest.mock import patch
from tools.audio.fal_qwen3_voice import FalQwen3Voice

class QwenTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        audio = self.root/'voice.wav'
        with wave.open(str(audio),'wb') as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(8000); f.writeframes(b'\0\0'*8000*3)
        self.inputs = {'operation':'clone','audio_path':str(audio),
                       'audio_sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),
                       'audio_url':'https://v3b.fal.media/files/test/voice.wav',
                       'job_path':str(self.root/'job.json'),'output_path':str(self.root/'clone.json')}
        self.tool = FalQwen3Voice(); self.rehash()
    def tearDown(self): self.temp.cleanup()
    def rehash(self):
        payload=self.tool.build_request(self.inputs)
        self.inputs['expected_payload_sha256']=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    def test_schema_and_hash(self):
        self.assertEqual(self.tool.build_request(self.inputs)['enable_safety_checker'],True)
        with self.assertRaisesRegex(ValueError,'hash'):
            self.tool.build_request(dict(self.inputs,audio_sha256='bad'))
        with self.assertRaisesRegex(ValueError,'CDN'):
            self.tool.build_request(dict(self.inputs,audio_url='https://evil.example/a.wav'))
    def test_unknown_never_replays(self):
        with patch.dict('os.environ',{'FAL_KEY':'fake'}), patch('tools.audio.fal_qwen3_voice.request_json',side_effect=TimeoutError) as req:
            self.assertFalse(self.tool.execute(self.inputs).success); self.assertFalse(self.tool.execute(self.inputs).success)
            self.assertEqual(req.call_count,1)
    def test_accepted_resume_never_posts_twice(self):
        accepted={'request_id':'fake','status_url':'https://queue.fal.run/s','response_url':'https://queue.fal.run/r'}
        with patch.dict('os.environ',{'FAL_KEY':'fake'}), patch('tools.audio.fal_qwen3_voice.request_json',return_value=accepted) as req, patch('tools.audio.fal_qwen3_voice.poll',side_effect=TimeoutError):
            self.assertFalse(self.tool.execute(self.inputs).success); self.assertFalse(self.tool.execute(self.inputs).success)
            self.assertEqual(req.call_count,1)
    def test_speech_payload_binds_embedding(self):
        embedding=self.root/'v.safetensors'; embedding.write_bytes(b'test')
        inputs={'operation':'speech','text':'Today the temperature fell.', 'embedding_path':str(embedding),
                'embedding_sha256':hashlib.sha256(embedding.read_bytes()).hexdigest(),
                'embedding_url':'https://storage.googleapis.com/falserverless/v.safetensors'}
        payload=self.tool.build_request(inputs)
        self.assertEqual(payload['language'],'English'); self.assertNotIn('prompt',payload)
        self.assertEqual(self.tool.estimate_cost(inputs),.15)
        embedding.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'hash'):
            self.tool.build_request(inputs)
    def test_completed_clone_downloads_private_bound_metadata(self):
        accepted={'request_id':'fake','status_url':'https://queue.fal.run/s','response_url':'https://queue.fal.run/r'}
        class Response:
            status_code=200
            def raise_for_status(self): pass
            def iter_content(self,chunk_size): yield b'fake-embedding'
        with patch.dict('os.environ',{'FAL_KEY':'fake'}), patch('tools.audio.fal_qwen3_voice.request_json',
                side_effect=[accepted,{'speaker_embedding':{'url':'https://storage.googleapis.com/falserverless/embed.safetensors'}}]), patch('tools.audio.fal_qwen3_voice.poll'), patch('requests.get',return_value=Response()):
            result=self.tool.execute(self.inputs)
        self.assertTrue(result.success,result.error)
        metadata=json.loads(Path(self.inputs['output_path']).read_text())
        self.assertEqual(metadata['request_id'],'fake')
        self.assertEqual(metadata['embedding_sha256'],hashlib.sha256(b'fake-embedding').hexdigest())
        self.assertEqual(Path(metadata['embedding_path']).read_bytes(),b'fake-embedding')

if __name__ == '__main__': unittest.main()
