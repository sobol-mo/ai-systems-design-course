import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from learning_project.cli import main
from learning_project.doctor import collect_environment_report


class Lab01DoctorTests(unittest.TestCase):
    @patch("learning_project.doctor._obsidian_available", return_value=True)
    @patch("learning_project.doctor._probe_command")
    @patch("learning_project.doctor._windows_build", return_value=26100)
    @patch("learning_project.doctor.platform.release", return_value="11")
    @patch("learning_project.doctor.platform.system", return_value="Windows")
    def test_collect_reports_a_green_windows_environment(
        self,
        _system,
        _release,
        _build,
        probe_command,
        _obsidian,
    ) -> None:
        probe_command.side_effect = [
            ("available", "git version 2.51.0"),
            ("available", "gh version 2.80.0"),
            ("available", "uv 0.12.9"),
            ("authenticated", "models available"),
        ]

        report = collect_environment_report()

        self.assertEqual(report["preflight"], "green")
        self.assertEqual(report["host"]["build"], 26100)
        self.assertEqual(report["capabilities"]["agy"]["status"], "authenticated")
        self.assertEqual(report["capabilities"]["obsidian"]["status"], "available")

    @patch("learning_project.doctor._obsidian_available", return_value=True)
    @patch("learning_project.doctor._probe_command")
    @patch("learning_project.doctor._windows_build", return_value=26100)
    @patch("learning_project.doctor.platform.release", return_value="11")
    @patch("learning_project.doctor.platform.system", return_value="Windows")
    def test_collect_reports_green_windows_without_agy(
        self,
        _system,
        _release,
        _build,
        probe_command,
        _obsidian,
    ) -> None:
        probe_command.side_effect = [
            ("available", "git version 2.51.0"),
            ("available", "gh version 2.80.0"),
            ("available", "uv 0.12.9"),
            ("unavailable", "command unavailable"),
        ]

        report = collect_environment_report()

        self.assertEqual(report["preflight"], "green")
        self.assertEqual(report["capabilities"]["agy"]["status"], "unavailable")

    @patch("learning_project.doctor._obsidian_available", return_value=True)
    @patch("learning_project.doctor._probe_command")
    @patch("learning_project.doctor.platform.release", return_value="6.8.0-139-generic")
    @patch("learning_project.doctor.platform.system", return_value="Linux")
    def test_collect_reports_a_green_linux_environment(
        self,
        _system,
        _release,
        probe_command,
        _obsidian,
    ) -> None:
        probe_command.side_effect = [
            ("available", "git version 2.51.0"),
            ("available", "gh version 2.80.0"),
            ("available", "uv 0.12.9"),
            ("unavailable", "command unavailable"),
        ]

        report = collect_environment_report()

        self.assertEqual(report["preflight"], "green")
        self.assertEqual(report["host"]["system"], "linux")
        self.assertIsNone(report["host"]["build"])
        self.assertEqual(report["capabilities"]["agy"]["status"], "unavailable")

    @patch("learning_project.doctor._obsidian_available", return_value=True)
    @patch("learning_project.doctor._probe_command")
    @patch("learning_project.doctor.platform.release", return_value="25.1")
    @patch("learning_project.doctor.platform.system", return_value="Darwin")
    def test_collect_reports_macos_red_even_with_capabilities(
        self,
        _system,
        _release,
        probe_command,
        _obsidian,
    ) -> None:
        probe_command.side_effect = [
            ("available", "git version 2.51.0"),
            ("available", "gh version 2.80.0"),
            ("available", "uv 0.12.9"),
            ("authenticated", "models available"),
        ]

        report = collect_environment_report()

        self.assertEqual(report["preflight"], "red")
        self.assertEqual(report["host"]["system"], "darwin")

    @patch("learning_project.cli.collect_environment_report")
    def test_doctor_writes_machine_readable_report_and_fails_red(self, collect) -> None:
        collect.return_value = {
            "schema_version": "1.0",
            "host": {"system": "windows", "release": "11", "build": 26100},
            "preflight": "red",
            "capabilities": {"agy": {"status": "authentication-required"}},
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "environment-report.json"

            code = main(["doctor", "--output", str(output)])

            self.assertEqual(code, 1)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), collect.return_value)


if __name__ == "__main__":
    unittest.main()
