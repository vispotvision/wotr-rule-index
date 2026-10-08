"""Reliability checks: evidence, stale context, locks, failures and resumption."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import writers_room as W


class RoomTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.job = Path(self.tmp.name)
        self.packet = {"type": "quiet", "culture": "Nalūn", "band": "standard",
                       "sources": {"canon.md": "The gutter must remain open."}}
        text = json.dumps(self.packet)
        (self.job / "packet.json").write_text(text)
        W.save(self.job / "state.json", {"stage": "prepared", "packet_sha256": W.digest(text), "events": []})
        self.args = argparse.Namespace(room=str(self.job), timeout=1, repairs=1)
        self.draft = "# Test\n\nShe opened the gutter. The old channel carried the water clear of the door."
        self.author = {"status": "ready", "draft": self.draft, "notes": "Draft test notes.", "dispositions": []}
        self.clean = {"fails": [], "warns": [], "info": []}

    def review(self, **changes):
        f = {"id": "gutter", "category": "rule", "blocking": True,
             "draft_quote": "opened the gutter", "source": "canon.md",
             "quote": "gutter must remain open", "explanation": "A test finding", "suggestion": "Keep it open"}
        f.update(changes)
        return {"verdict": "revise", "findings": [f]}

    def test_blockers_require_real_source_and_draft_quotes(self):
        W.validate_review(self.review(), self.packet, self.draft, "codex")
        for changes in ({"quote": "invented prohibition"}, {"draft_quote": "not in draft"},
                        {"source": "missing.md"}, {"category": "style"}, {"category": "unsupported"}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                W.validate_review(self.review(**changes), self.packet, self.draft, "codex")

    def test_optional_style_does_not_need_canon(self):
        W.validate_review(self.review(category="style", blocking=False, source="", quote=""), self.packet, self.draft, "gemini")

    def test_mutual_exclusion(self):
        with W.lock(self.job / ".lock"), self.assertRaises(ValueError):
            with W.lock(self.job / ".lock"):
                pass

    def test_packet_drift_stops_before_dispatch(self):
        (self.job / "packet.json").write_text("{}")
        with patch.object(W, "worker") as worker, self.assertRaises(ValueError):
            W.run_room(self.args)
        worker.assert_not_called()

    def test_completed_stages_resume_without_duplicate_calls(self):
        W.save(self.job / "author-r0.json", self.author)
        def answer(role, *args):
            return {"verdict": "ready", "findings": [], "protect": "gutter"}
        with patch.object(W, "worker", side_effect=answer) as worker, patch.object(W, "verify_draft", return_value=self.clean):
            W.run_room(self.args)
            self.assertEqual(sorted(c.args[0] for c in worker.call_args_list), ["codex", "gemini"])
            worker.reset_mock()
            W.run_room(self.args)
            worker.assert_not_called()
        self.assertEqual((self.job / "final.md").read_text(), self.draft)

    def test_worker_failure_never_becomes_ready(self):
        with patch.object(W, "worker", side_effect=ValueError("offline")), self.assertRaises(ValueError):
            W.run_room(self.args)
        self.assertEqual(json.loads((self.job / "state.json").read_text())["stage"], "needs_attention")
        self.assertFalse((self.job / "final.md").exists())

    def test_invalid_author_response_is_not_cached_as_completed(self):
        with patch.object(W, "worker", return_value={"status": "needs_context", "notes": "Missing facts"}), self.assertRaises(ValueError):
            W.run_room(self.args)
        self.assertTrue((self.job / "author-r0.rejected.json").exists())
        self.assertFalse((self.job / "author-r0.json").exists())

    def test_redo_review_invalidates_final_and_downstream(self):
        W.save(self.job / "author-r0.json", self.author)
        for role in ("codex", "gemini"):
            W.save(self.job / f"{role}-review.json", {"verdict": "ready", "findings": []})
        (self.job / "final.md").write_text("Stale final")
        self.args.redo = "gemini-review"
        with patch.object(W, "worker", return_value={"verdict": "ready", "findings": []}) as worker, patch.object(W, "verify_draft", return_value=self.clean):
            W.run_room(self.args)
        self.assertEqual([c.args[0] for c in worker.call_args_list], ["gemini"])
        self.assertEqual((self.job / "final.md").read_text(), self.draft)

    def test_failed_verification_has_bounded_repairs(self):
        calls = []
        def answer(role, *args):
            calls.append(role)
            return deepcopy(self.author) if role == "claude" else {"verdict": "ready", "findings": []}
        bad = {"fails": ["bad"], "warns": [], "info": []}
        with patch.object(W, "worker", side_effect=answer), patch.object(W, "verify_draft", return_value=bad), self.assertRaises(ValueError):
            W.run_room(self.args)
        self.assertEqual(calls.count("claude"), 3)  # original, review revision, one mechanical repair
        self.assertFalse((self.job / "final.md").exists())

    def test_private_pages_and_secret_urls_do_not_enter_packets(self):
        root = self.job / "repo"
        (root / "wiki").mkdir(parents=True)
        (root / "wiki/.manifest.json").write_text(json.dumps({"x": {"rel": "hidden.md", "private": True}}))
        (root / "wiki/hidden.md").write_text("Private material")
        (root / "wiki/public.md").write_text("Secret route /t/example-token/path")
        with patch.object(W, "ROOT", root):
            for name in ("wiki/hidden.md", "wiki/public.md", "../outside.md"):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    W.source_text(Path(name))

    def test_feedback_is_append_only_and_scoped(self):
        f = self.job / "feedback.jsonl"
        a = argparse.Namespace(scene="scene-one", kind="liked", scope="scene", text="Isaac's exact reaction", quote="", supersedes="")
        with patch.object(W, "FEEDBACK", f):
            W.record_feedback(a)
            first = f.read_text()
            a.supersedes = json.loads(first)["id"]
            a.kind = "correction"
            W.record_feedback(a)
            self.assertTrue(f.read_text().startswith(first))
            self.assertEqual(len(f.read_text().splitlines()), 2)
            self.assertEqual(json.loads(W.feedback_text("another-scene")), [])
            effective = json.loads(W.feedback_text("scene-one"))
            self.assertEqual(len(effective), 1)
            self.assertEqual(effective[0]["kind"], "correction")
            a.supersedes = "missing"
            with self.assertRaises(ValueError):
                W.record_feedback(a)


if __name__ == "__main__":
    unittest.main()
