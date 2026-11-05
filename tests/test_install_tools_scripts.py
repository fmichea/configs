import json
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest
from conftest import FAKE_BIN, PYTHON_DIR

HOME_SOURCE = Path(__file__).resolve().parent.parent / "home"

# (script, tool it runs, expected calls; the last argument of each is a prefix, before the version)
SCRIPTS = [
    (
        "run_onchange_after_install-go-tools.sh",
        "go",
        [["install", "golang.org/x/tools/gopls@v"]],
    ),
    (
        "run_onchange_after_install-python-tools.sh",
        "uv",
        [["tool", "install", "keygate=="], ["tool", "install", "ruff=="]],
    ),
]


@pytest.fixture
def run_script(tmp_path) -> Callable[[str, str, bool], list[list[str]]]:
    """run_script(script, tool, with_tool) runs the script, returns the fake tool's calls."""
    calls = tmp_path / "calls.jsonl"
    calls.touch()

    # No system directories on PATH: a real tool there (/usr/bin/go on Arch) would
    # run instead of the fake one, or stop the script from skipping.
    def run_script(script: str, tool: str, with_tool: bool) -> list[list[str]]:
        env = {
            "HOME": str(tmp_path),
            "PATH": f"{FAKE_BIN}:{PYTHON_DIR}" if with_tool else str(tmp_path),
            f"FAKE_{tool.upper()}_CALLS": str(calls),
        }
        subprocess.run(["/bin/sh", str(HOME_SOURCE / script)], env=env, check=True)
        return [json.loads(line) for line in calls.read_text().splitlines()]

    return run_script


@pytest.mark.parametrize(("script", "tool", "expected"), SCRIPTS)
def test_installs_pinned_version_with_tool(run_script, script, tool, expected):
    calls = run_script(script, tool, with_tool=True)

    assert [call[:-1] for call in calls] == [call[:-1] for call in expected]
    assert all(
        call[-1].startswith(prefix[-1]) for call, prefix in zip(calls, expected, strict=True)
    )


@pytest.mark.parametrize(("script", "tool", "expected"), SCRIPTS)
def test_skips_without_tool(run_script, script, tool, expected):
    assert run_script(script, tool, with_tool=False) == []
