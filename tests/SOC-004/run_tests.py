"""Offline byte-integrity, full-output replay and v2 error-behavior checks."""
import hashlib
from contextlib import contextmanager
from pathlib import Path
import platform
import subprocess
import shutil
import sys
import unittest
import uuid

sys.dont_write_bytecode = True
from generate_fixtures import CASES, fixture_bytes

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "evidence/SOC-004"
SOURCES = [ROOT / "detections/SOC-004/ssh_detector.py", EVIDENCE / "ssh_detector.py"]
V2 = ROOT / "detections/SOC-004/ssh_detector_v2.py"
FIXTURES = Path(__file__).parent / "fixtures"
SCRATCH = ROOT / "local-output"
ORIGINAL = {
    "ssh-repeated-failures.log": "ssh-detection-alert.log",
    "ssh-negative-test.log": "ssh-negative-test-result.log",
    "ssh-boundary-test.log": "ssh-boundary-test-result.log",
    "ssh-exact-boundary-test.log": "ssh-exact-boundary-test-result.log",
}


def normalized(content):
    return content.replace("\r\n", "\n")


def run(source, input_path):
    return subprocess.run([sys.executable, "-B", str(source), str(input_path)], capture_output=True, text=True, encoding="utf-8", timeout=10)


@contextmanager
def temporary_inputs():
    # Inherit workspace permissions; Windows sandboxed Python 3.14 mkdtemp ACLs
    # can deny access even to their creating process. These are artificial inputs.
    directory = SCRATCH / f"soc004-{uuid.uuid4().hex}"
    directory.mkdir()
    try:
        yield directory
    finally:
        if not directory.resolve().is_relative_to(SCRATCH.resolve()):
            raise RuntimeError("Refusing cleanup outside local-output")
        shutil.rmtree(directory)


class DetectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        SCRATCH.mkdir(exist_ok=True)

    def assert_output(self, source, input_path, expected):
        result = run(source, input_path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(normalized(result.stdout), normalized(expected))
        if source == V2:
            self.assertIn("Records read:", result.stderr)
        else:
            self.assertEqual(result.stderr, "")

    def test_original_manifest_and_source_relationship(self):
        rows = (EVIDENCE / "SHA256SUMS.txt").read_text().splitlines()
        self.assertEqual(len(rows), 10)
        for row in rows:
            digest, name = row.split()
            with self.subTest(artifact=name):
                self.assertEqual(hashlib.sha256((EVIDENCE / name).read_bytes()).hexdigest(), digest)
        self.assertEqual(SOURCES[1].read_bytes(), b"\n" + SOURCES[0].read_bytes() + b"\n\n")
        self.assertEqual((EVIDENCE / "ssh-negative-test.log").read_bytes(), b"".join((EVIDENCE / "ssh-repeated-failures.log").read_bytes().splitlines(keepends=True)[:2]))

    def test_syntax_without_cache(self):
        for source in [*SOURCES, V2]:
            with self.subTest(source=str(source.relative_to(ROOT))):
                compile(source.read_bytes(), str(source), "exec")

    def test_original_complete_saved_outputs(self):
        for source in [*SOURCES, V2]:
            for input_name, output_name in ORIGINAL.items():
                with self.subTest(source=str(source.relative_to(ROOT)), input=input_name):
                    self.assert_output(source, EVIDENCE / input_name, (EVIDENCE / output_name).read_text())

    def test_preserved_new_synthetic_fixtures(self):
        expected_files = fixture_bytes()
        self.assertEqual({p.name for p in FIXTURES.iterdir() if p.is_file()}, set(expected_files))
        for name, content in expected_files.items():
            with self.subTest(file=name):
                self.assertEqual((FIXTURES / name).read_bytes(), content)
        for source in [*SOURCES, V2]:
            for name in CASES:
                with self.subTest(source=str(source.relative_to(ROOT)), case=name):
                    self.assert_output(source, FIXTURES / f"{name}.log", (FIXTURES / f"{name}.expected.txt").read_text())

    def test_v2_invalid_user_and_skip_reporting(self):
        text = (FIXTURES / "within-window.log").read_text().replace("Failed password for test-analyst", "Failed password for invalid user test-analyst")
        with temporary_inputs() as directory:
            self.assertTrue(Path(directory).resolve().is_relative_to(SCRATCH.resolve()))
            path = Path(directory) / "input.log"
            path.write_text("unrelated journal record\n" + text)
            result = run(V2, path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(normalized(result.stdout), (FIXTURES / "within-window.expected.txt").read_text())
            self.assertIn("Records read: 4; matched: 3; skipped: 1", result.stderr)

    def test_v2_failures_never_print_clean_result(self):
        good = (FIXTURES / "within-window.log").read_text()
        cases = {
            "malformed-timestamp": good.replace("2000-01-01T00:00:00+00:00", "not-a-date"),
            "naive-timestamp": good.replace("+00:00", ""),
            "mixed-aware-naive": good.replace("2000-01-01T00:00:30+00:00", "2000-01-01T00:00:30"),
            "malformed-failure": good.replace("port 40000", "port unknown"),
        }
        with temporary_inputs() as directory:
            self.assertTrue(Path(directory).resolve().is_relative_to(SCRATCH.resolve()))
            path = Path(directory) / "input.log"
            for name, content in cases.items():
                with self.subTest(case=name):
                    path.write_text(content)
                    result = run(V2, path)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertIn("ERROR:", result.stderr)
            path.write_bytes(b"\xff")
            for name, target in [("invalid-utf8", path), ("missing-file", Path(directory) / "absent.log"), ("directory", Path(directory))]:
                with self.subTest(case=name):
                    result = run(V2, target)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertIn("ERROR:", result.stderr)

    def test_v2_empty_and_all_skipped_inputs(self):
        with temporary_inputs() as directory:
            self.assertTrue(Path(directory).resolve().is_relative_to(SCRATCH.resolve()))
            path = Path(directory) / "input.log"
            for content, summary in [("", "Records read: 0; matched: 0; skipped: 0"), ("unrelated\n", "Records read: 1; matched: 0; skipped: 1")]:
                with self.subTest(input=content):
                    path.write_text(content)
                    result = run(V2, path)
                    self.assertEqual(result.returncode, 0)
                    self.assertIn(summary, result.stderr)
                    self.assertIn("Events parsed: 0", result.stdout)


if __name__ == "__main__":
    print(f"Runtime: Python {platform.python_version()} on {platform.system()}", flush=True)
    print("Replay coverage: 8 historical-source original outputs, 4 v2 original outputs, 21 new synthetic outputs; original SHA256 10/10 required.", flush=True)
    unittest.main(verbosity=2)
