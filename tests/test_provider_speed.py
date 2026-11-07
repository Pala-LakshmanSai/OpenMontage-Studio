import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("provider_speed", Path(__file__).resolve().parents[1] / "scripts/provider_speed.py")
speed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(speed)


def event(kind, at, job="j1", **extra):
    return dict(event_id=f"{job}:{kind}", event=kind, provider="kreatorflow", workspace="test-alias", pass_id="pass1", project_id="film1", job_id=job, observed_at=at, model="seedance_2_5", duration_seconds=30, resolution="720p", route="studio", aspect_ratio="16:9", generate_audio=True, credit_free=True, **extra)


class ProviderSpeedTests(unittest.TestCase):
    def test_idempotence_conflict_and_no_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            item = event("admitted", "2026-11-07T06:00:00Z")
            self.assertTrue(speed.record(path, item)["recorded"])
            self.assertTrue(speed.record(path, item)["duplicate"])
            with self.assertRaisesRegex(ValueError, "Conflicting"):
                speed.record(path, dict(item, duration_seconds=8))
            self.assertEqual(len(path.read_text().splitlines()), 1)

    def test_partial_progress_never_invents_start(self):
        item = event("progress_observed", "2026-11-07T06:03:00Z", elapsed_seconds=183, countdown_seconds=131, progress_percent=67)
        job = speed.report([item])["cohorts"][0]["jobs"][0]
        self.assertTrue(job["partial_observation"])
        self.assertNotIn("total_seconds", job)
        self.assertEqual(job["latest_progress"]["elapsed_seconds"], 183)

    def test_like_settings_and_unmixed_timestamp_basis(self):
        rows = [event("admitted", "2026-11-07T06:00:03Z", occurred_at="2026-11-07T06:00:00Z", allowance_state="fast"),
                event("render_started", "2026-11-07T06:00:15Z", occurred_at="2026-11-07T06:00:10Z"),
                event("completed", "2026-11-07T06:01:04Z", occurred_at="2026-11-07T06:01:00Z"),
                event("admitted", "2026-11-07T06:02:00Z", job="j2", allowance_state="relaxed"),
                event("completed", "2026-11-07T06:04:00Z", job="j2"),
                event("admitted", "2026-11-07T06:05:00Z", job="j3", occurred_at="2026-11-07T06:04:55Z", allowance_state="fast"),
                event("completed", "2026-11-07T06:06:00Z", job="j3")]
        cohort = speed.report(rows)["cohorts"][0]
        self.assertEqual(cohort["jobs"][0]["queue_seconds"], 10)
        self.assertEqual(cohort["jobs"][0]["render_seconds"], 50)
        self.assertEqual(cohort["jobs"][2]["total_seconds"], 60)
        self.assertEqual(cohort["jobs"][2]["total_basis"], "observation_times")
        self.assertEqual(cohort["admissions_observed_before_first_relaxed"], 1)
        self.assertIsNone(cohort["exact_fast_allowance_quota"])
        observed = next(c for c in cohort["comparisons"] if c["settings"][-1] == "observation_times")
        self.assertEqual(observed["relaxed_to_fast_ratio"], 2)
        self.assertEqual(cohort["completed_nominal_seconds"], 90)

    def test_reject_secrets_and_naive_timestamps(self):
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            speed.validate(event("admitted", "2026-11-07T06:00:00Z", api_key="secret"))
        with self.assertRaisesRegex(ValueError, "No credentials"):
            speed.validate(event("admitted", "2026-11-07T06:00:00Z", note="Bearer secret"))
        with self.assertRaisesRegex(ValueError, "timezone"):
            speed.validate(event("admitted", "2026-11-07T06:00:00"))

if __name__ == "__main__":
    unittest.main()
