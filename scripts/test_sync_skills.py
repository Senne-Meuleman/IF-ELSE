"""Behavioral checks for skill synchronization; python -m unittest discover -s scripts."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sync_skills


class SyncSkillsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.target = self.root / "target"
        self.skill = self.source / "example" / "SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text(
            "---\nname: example\ndescription: A sample workflow.\n---\nUse it.\n",
            encoding="utf-8",
        )
        self.addCleanup(patch.stopall)
        patch.object(sync_skills, "SOURCE", self.source).start()
        patch.object(sync_skills, "TARGET", self.target).start()

    def run_sync(self, *args: str) -> int:
        with patch("sys.argv", ["sync_skills.py", *args]), contextlib.redirect_stdout(io.StringIO()):
            return sync_skills.main()

    def test_check_does_not_write_missing_target(self) -> None:
        self.assertEqual(self.run_sync("--check"), 1)
        self.assertFalse(self.target.exists())

    def test_sync_copies_binary_assets_and_is_idempotent(self) -> None:
        asset = self.skill.parent / "assets" / "sample.bin"
        asset.parent.mkdir()
        asset.write_bytes(bytes(range(256)))
        self.assertEqual(self.run_sync(), 0)
        copied = self.target / "example" / "assets" / "sample.bin"
        self.assertEqual(copied.read_bytes(), asset.read_bytes())
        before = copied.stat().st_mtime_ns
        self.assertEqual(self.run_sync(), 0)
        self.assertEqual(copied.stat().st_mtime_ns, before)
        self.assertEqual(self.run_sync("--check"), 0)

    def test_drift_detected_and_repaired(self) -> None:
        self.run_sync()
        self.skill.write_text(self.skill.read_text() + "New guidance.\n")
        self.assertEqual(self.run_sync("--check"), 1)
        self.assertEqual(self.run_sync(), 0)
        self.assertEqual(self.run_sync("--check"), 0)

    def test_unexpected_target_preserved(self) -> None:
        self.run_sync()
        unexpected = self.target / "teammate.txt"
        unexpected.write_text("keep me")
        self.assertEqual(self.run_sync(), 1)
        self.assertEqual(unexpected.read_text(), "keep me")

    def test_missing_resource_rejected_before_writing(self) -> None:
        self.skill.write_text(self.skill.read_text() + "Read `references/missing.md`.\n")
        with self.assertRaisesRegex(ValueError, "missing resource"):
            self.run_sync()
        self.assertFalse(self.target.exists())

    def test_crlf_source_is_not_drift(self) -> None:
        self.run_sync()
        lf = self.skill.read_bytes().replace(b"\r\n", b"\n")
        self.skill.write_bytes(lf.replace(b"\n", b"\r\n"))
        self.assertEqual(self.run_sync("--check"), 0)
        copied = self.target / "example" / "SKILL.md"
        self.assertNotIn(b"\r\n", copied.read_bytes())

    def test_mismatched_name_rejected(self) -> None:
        self.skill.write_text(self.skill.read_text().replace("name: example", "name: other"))
        with self.assertRaisesRegex(ValueError, "must match"):
            self.run_sync()


if __name__ == "__main__":
    unittest.main()
