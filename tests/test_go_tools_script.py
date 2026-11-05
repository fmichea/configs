import json
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

from conftest import FAKE_BIN, PYTHON_DIR

HOME_SOURCE = Path(__file__).resolve().parent.parent / "home"
SCRIPT = HOME_SOURCE / "run_onchange_after_install-go-tools.sh"


@pytest.fixture
def run_script(tmp_path) -> Callable[[bool], list[list[str]]]:
    """run_script(with_go) runs the script and returns the fake go's calls."""
    go_calls = tmp_path / "go-calls.jsonl"
    go_calls.touch()

    # No system directories on PATH: a real go there (/usr/bin/go on Arch) would
    # run instead of the fake one, or stop the script from skipping.
    def run_script(with_go: bool) -> list[list[str]]:
        env = {
            "HOME": str(tmp_path),
            "PATH": f"{FAKE_BIN}:{PYTHON_DIR}" if with_go else str(tmp_path),
            "FAKE_GO_CALLS": str(go_calls),
        }
        subprocess.run(["/bin/sh", str(SCRIPT)], env=env, check=True)
        return [json.loads(line) for line in go_calls.read_text().splitlines()]

    return run_script


def test_installs_gopls_with_go(run_script):
    calls = run_script(with_go=True)

    assert len(calls) == 1
    assert calls[0][0] == "install"
    assert calls[0][1].startswith("golang.org/x/tools/gopls@v")


def test_skips_without_go(run_script):
    assert run_script(with_go=False) == []
