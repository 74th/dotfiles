import contextlib
import importlib.machinery
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


loader = importlib.machinery.SourceFileLoader(
    "super_update", str(Path(__file__).resolve().parents[1] / "bin" / "super-update")
)
spec = importlib.util.spec_from_loader(loader.name, loader)
super_update = importlib.util.module_from_spec(spec)
sys.modules[loader.name] = super_update
loader.exec_module(super_update)


class SuperUpdateTests(unittest.TestCase):
    def test_install_or_update_based_on_command_presence(self):
        for name, installer in (
            ("claude", "curl -fsSL https://claude.ai/install.sh | bash"),
            ("codex", "curl -fsSL https://chatgpt.com/codex/install.sh | sh"),
        ):
            for installed in (False, True):
                with (
                    self.subTest(name=name, installed=installed),
                    mock.patch.object(
                        super_update.shutil, "which", return_value="/mock/bin" if installed else None
                    ) as which,
                    mock.patch.object(super_update.subprocess, "run") as run,
                    contextlib.redirect_stdout(io.StringIO()),
                ):
                    run.return_value.returncode = 0
                    self.assertTrue(super_update.update(name, "linux"))
                    which.assert_called_with(name)
                    expected = [name, "update"] if installed else super_update.shell_pipe(installer)
                    run.assert_called_once_with(expected)

    def test_same_steps_are_used_when_install_and_update_are_identical(self):
        for installed in (False, True):
            with (
                self.subTest(installed=installed),
                mock.patch.object(
                    super_update.shutil, "which", return_value="/mock/volta" if installed else None
                ),
                mock.patch.object(super_update.subprocess, "run") as run,
                mock.patch.dict(os.environ, {"PATH": "/mock/path"}),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                run.return_value.returncode = 0
                self.assertTrue(super_update.update("volta", "linux"))
                self.assertEqual(
                    [call.args[0] for call in run.call_args_list],
                    [
                        super_update.shell_pipe("curl -fsSL https://get.volta.sh | bash"),
                        ["volta", "install", "node"],
                    ],
                )

    def test_install_failure_is_reported(self):
        stderr = io.StringIO()
        with (
            mock.patch.object(super_update.shutil, "which", return_value=None),
            mock.patch.object(super_update.subprocess, "run") as run,
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(stderr),
        ):
            run.return_value.returncode = 1
            self.assertFalse(super_update.update("codex", "linux"))
        self.assertIn("codex: failed:", stderr.getvalue())

    def test_codex_cli_installs_then_updates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bindir = root / "bin"
            bindir.mkdir()
            log = root / "calls"
            curl = bindir / "curl"
            curl.write_text('#!/bin/sh\nprintf \'echo install >> "$CALL_LOG"\\n\'\n')
            curl.chmod(0o755)
            env = {
                **os.environ,
                "HOME": str(root),
                "PATH": f"{bindir}{os.pathsep}/usr/bin:/bin",
                "CALL_LOG": str(log),
                "PYTHONDONTWRITEBYTECODE": "1",
            }
            script = str(Path(__file__).resolve().parents[1] / "bin" / "super-update")
            result = subprocess.run(
                [sys.executable, script, "codex"], env=env, capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(log.read_text().splitlines(), ["install"])

            codex = bindir / "codex"
            codex.write_text('#!/bin/sh\nprintf "codex %s\\n" "$*" >> "$CALL_LOG"\n')
            codex.chmod(0o755)
            result = subprocess.run(
                [sys.executable, script, "codex"], env=env, capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(log.read_text().splitlines(), ["install", "codex update"])

    def run_update(self, *, installed=False, fallback=False, fail=None, count=1):
        state = {"installed": installed}
        calls = []

        def which(command):
            if command != "volta" or not state["installed"]:
                return None
            bin_dir = str(super_update.TOOL_MAP["volta"].bin_dir)
            if fallback and bin_dir not in os.environ["PATH"].split(os.pathsep):
                return None
            return "/mock/volta"

        def run(command, **kwargs):
            calls.append(command)
            if command[0] == "bash" and fail != "installer":
                state["installed"] = True
            if fail == "installer" and command[0] == "bash":
                return subprocess.CompletedProcess(command, 1)
            if fail == "node" and command[-1] == "node":
                return subprocess.CompletedProcess(command, 1)
            return subprocess.CompletedProcess(command, 0)

        with (
            mock.patch.dict(os.environ, {"PATH": "/mock/path"}),
            mock.patch.object(super_update.shutil, "which", side_effect=which),
            mock.patch.object(super_update.subprocess, "run", side_effect=run),
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            results = [super_update.update("openspec", "linux") for _ in range(count)]
        return results, calls

    def test_installs_dependency_before_openspec_once(self):
        results, calls = self.run_update(count=2)
        self.assertEqual(results, [True, True])
        self.assertEqual(
            calls,
            [
                super_update.TOOL_MAP["volta"].steps[0].cmd,
                ["volta", "install", "node"],
                ["volta", "install", "@fission-ai/openspec@latest"],
                ["volta", "install", "@fission-ai/openspec@latest"],
            ],
        )

    def test_existing_volta_on_path_or_fallback_is_not_reinstalled(self):
        for fallback in (False, True):
            with self.subTest(fallback=fallback):
                results, calls = self.run_update(installed=True, fallback=fallback)
                self.assertEqual(results, [True])
                self.assertEqual(calls, [["volta", "install", "@fission-ai/openspec@latest"]])

    def test_dependency_failure_stops_openspec(self):
        for failure, expected_calls in (("installer", 1), ("node", 2)):
            with self.subTest(failure=failure):
                results, calls = self.run_update(fail=failure)
                self.assertEqual(results, [False])
                self.assertEqual(len(calls), expected_calls)
                self.assertNotIn(["volta", "install", "@fission-ai/openspec@latest"], calls)

    def test_fallback_path_is_passed_to_volta(self):
        with (
            mock.patch.dict(os.environ, {"PATH": "/mock/path"}),
            mock.patch.object(super_update.shutil, "which", return_value=None),
            mock.patch.object(super_update.subprocess, "run") as run,
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            run.return_value.returncode = 0
            self.assertTrue(super_update.update("openspec", "linux"))
            bin_dir = str(super_update.TOOL_MAP["volta"].bin_dir)
            self.assertEqual(os.environ["PATH"], f"{bin_dir}{os.pathsep}/mock/path")

    def test_unsupported_os_does_not_install_dependency(self):
        tool = super_update.Tool("limited", {"linux": []}, dependencies=["volta"])
        with (
            mock.patch.dict(super_update.TOOL_MAP, {"limited": tool}),
            mock.patch.object(super_update.subprocess, "run") as run,
            contextlib.redirect_stderr(io.StringIO()),
        ):
            self.assertFalse(super_update.update("limited", "windows"))
        run.assert_not_called()

    def test_dependency_cycle_fails(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertFalse(super_update.update("openspec", "linux", ("openspec",)))

    def test_dependency_uses_configured_command(self):
        dependency = super_update.Tool("package", [super_update.Step(["install"])], command="binary")
        tool = super_update.Tool("target", [super_update.Step(["target"])], dependencies=["package"])
        with (
            mock.patch.dict(super_update.TOOL_MAP, {"package": dependency, "target": tool}),
            mock.patch.object(super_update.shutil, "which", return_value="/mock/binary") as which,
            mock.patch.object(super_update.subprocess, "run") as run,
            contextlib.redirect_stdout(io.StringIO()),
        ):
            run.return_value.returncode = 0
            self.assertTrue(super_update.update("target", "linux"))
            which.assert_called_with("binary")
            run.assert_called_once_with(["target"])


if __name__ == "__main__":
    unittest.main()
