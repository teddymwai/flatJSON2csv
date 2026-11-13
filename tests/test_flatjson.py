"""Unit and regression tests for flatJSON2csv."""

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

csv.field_size_limit(sys.maxsize)

from converter import discover_inputs, load_config, run_conversion, DEFAULTS

CLI_SCRIPT = str(ROOT_DIR / "flatJSON2csv.py")


def _find_sample(name: str) -> Path | None:
    candidates = [
        ROOT_DIR / "samples" / name,
        ROOT_DIR / name,
        Path("samples") / name,
        Path(name),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


class FlatJsonTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_single_root_object(self):
        in_file = self.dir_path / "single.json"
        out_file = self.dir_path / "single.csv"
        in_file.write_text(json.dumps({"name": "Alice", "role": "admin"}))

        cols = run_conversion(in_file, out_file, DEFAULTS.copy())
        self.assertEqual(sorted(cols), ["name", "role"])

        with out_file.open(newline="") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 1)
            self.assertEqual(reader[0]["name"], "Alice")
            self.assertEqual(reader[0]["role"], "admin")

    def test_array_of_objects(self):
        in_file = self.dir_path / "array.json"
        out_file = self.dir_path / "array.csv"
        in_file.write_text(json.dumps([{"id": 1, "val": "a"}, {"id": 2, "val": "b"}]))

        cols = run_conversion(in_file, out_file, DEFAULTS.copy())
        self.assertEqual(sorted(cols), ["id", "val"])

        with out_file.open(newline="") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 2)
            self.assertEqual(reader[1]["id"], "2")
            self.assertEqual(reader[1]["val"], "b")

    def test_array_of_primitives(self):
        in_file = self.dir_path / "primitives.json"
        out_file = self.dir_path / "primitives.csv"
        in_file.write_text(json.dumps([10, 20, 30]))

        cols = run_conversion(in_file, out_file, DEFAULTS.copy())
        self.assertEqual(cols, ["value"])

        with out_file.open(newline="") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 3)
            self.assertEqual([r["value"] for r in reader], ["10", "20", "30"])

    def test_enveloped_array_auto_detection(self):
        in_file = self.dir_path / "enveloped.json"
        out_file = self.dir_path / "enveloped.csv"
        in_file.write_text(json.dumps({
            "status": "ok",
            "data": {
                "results": [
                    {"code": "C1", "active": True},
                    {"code": "C2", "active": False}
                ]
            }
        }))

        cols = run_conversion(in_file, out_file, DEFAULTS.copy())
        self.assertEqual(sorted(cols), ["active", "code"])

        with out_file.open(newline="") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 2)
            self.assertEqual(reader[0]["code"], "C1")
            self.assertEqual(reader[0]["active"], "true")

    def test_ndjson(self):
        in_file = self.dir_path / "stream.ndjson"
        out_file = self.dir_path / "stream.csv"
        in_file.write_text('{"user": "u1", "score": 95}\n{"user": "u2", "score": 88}\n')

        cols = run_conversion(in_file, out_file, DEFAULTS.copy())
        self.assertEqual(sorted(cols), ["score", "user"])

        with out_file.open(newline="") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 2)
            self.assertEqual(reader[0]["user"], "u1")
            self.assertEqual(reader[1]["score"], "88")

    def test_cli_omitted_output_flag(self):
        in_file = self.dir_path / "auto_out.json"
        expected_csv = self.dir_path / "auto_out.csv"
        in_file.write_text(json.dumps({"msg": "hello"}))

        result = subprocess.run(
            [sys.executable, CLI_SCRIPT, str(in_file)],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue(expected_csv.exists())
        self.assertIn("msg", expected_csv.read_text())

    def test_cli_dry_run_no_output_flag(self):
        in_file = self.dir_path / "dry_run.json"
        in_file.write_text(json.dumps({"metric": 42}))

        result = subprocess.run(
            [sys.executable, CLI_SCRIPT, "--dry-run", str(in_file)],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("metric", result.stdout)

    def test_real_cyberec_scenario(self):
        source = _find_sample("cyberec_scenario.json")
        if not source:
            self.skipTest("cyberec_scenario.json not found")
        target = self.dir_path / "cyberec_test.csv"
        cols = run_conversion(source, target, DEFAULTS.copy())
        self.assertEqual(len(cols), 39)
        with target.open(newline="", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 1050)
            self.assertEqual(reader[0]["id"], "6ae055aae3932d60d529468c")

    def test_real_iev3_cloudtemplates(self):
        source = _find_sample("iev3_cloudtemplates_616.json")
        if not source:
            self.skipTest("iev3_cloudtemplates_616.json not found")
        target = self.dir_path / "iev3_test.csv"
        cols = run_conversion(source, target, DEFAULTS.copy())
        self.assertEqual(len(cols), 35)
        with target.open(newline="", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 616)
            self.assertEqual(reader[0]["id"], "6aeb9b79929abf0c73fbba1b")

    def test_real_iev2_cloudtemplates(self):
        source = _find_sample("iev2_cloudtemplates_1114.json")
        if not source:
            self.skipTest("iev2_cloudtemplates_1114.json not found")
        target = self.dir_path / "iev2_test.csv"
        cols = run_conversion(source, target, DEFAULTS.copy())
        self.assertEqual(len(cols), 37)
        with target.open(newline="", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 1114)
            self.assertEqual(reader[0]["id"], "6ad760e97953542e8b61efb1")

    def test_xlsx_export(self):
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl not installed")

        in_file = self.dir_path / "records.json"
        out_xlsx = self.dir_path / "records.xlsx"
        in_file.write_text(json.dumps([
            {"id": "U1", "name": "Alice", "score": 95, "active": True},
            {"id": "U2", "name": "Bob", "score": 88, "active": False}
        ]))

        cols = run_conversion(in_file, out_xlsx, DEFAULTS.copy())
        self.assertEqual(sorted(cols), ["active", "id", "name", "score"])
        self.assertTrue(out_xlsx.exists())

        wb = openpyxl.load_workbook(out_xlsx)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], ("active", "id", "name", "score"))
        self.assertEqual(rows[1], (True, "U1", "Alice", 95))
        self.assertEqual(rows[2], (False, "U2", "Bob", 88))

    def test_cli_xlsx_format_flag(self):
        try:
            import openpyxl
        except ImportError:
            self.skipTest("openpyxl not installed")

        in_file = self.dir_path / "test_cli.json"
        expected_xlsx = self.dir_path / "test_cli.xlsx"
        in_file.write_text(json.dumps([{"metric": "latency", "val": 12}]))

        result = subprocess.run(
            [sys.executable, CLI_SCRIPT, str(in_file), "--format", "xlsx"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue(expected_xlsx.exists())

        wb = openpyxl.load_workbook(expected_xlsx)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ("metric", "val"))
        self.assertEqual(rows[1], ("latency", 12))


if __name__ == "__main__":
    unittest.main()
