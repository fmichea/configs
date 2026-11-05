import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

NVM_SH = Path(__file__).resolve().parent.parent / "home" / "dot_zsh" / "nvm.sh"

# Stands in for nvm.sh: records how it is sourced and each nvm call.
FAKE_NVM_SH = """\
print -r -- "sourced $*" >> "$NVM_DIR/calls"
nvm() { print -r -- "nvm $*" >> "$NVM_DIR/calls" }
"""


class FakeNvm:
    """An NVM_DIR with installed node versions and a fake nvm.sh."""

    def __init__(self, nvm_dir: Path):
        self.dir = nvm_dir
        nvm_dir.mkdir()
        (nvm_dir / "nvm.sh").write_text(FAKE_NVM_SH)
        (nvm_dir / "calls").touch()

    def install(self, *versions: str) -> None:
        for version in versions:
            (self.dir / "versions" / "node" / version / "bin").mkdir(parents=True)

    def set_default(self, alias: str) -> None:
        (self.dir / "alias").mkdir(exist_ok=True)
        (self.dir / "alias" / "default").write_text(f"{alias}\n")

    def bin(self, version: str) -> str:
        return str(self.dir / "versions" / "node" / version / "bin")

    def calls(self) -> list[str]:
        return (self.dir / "calls").read_text().splitlines()


@pytest.fixture
def home(tmp_path) -> Path:
    home = tmp_path / "home"
    home.mkdir()
    return home


@pytest.fixture
def nvm(home) -> FakeNvm:
    return FakeNvm(home / ".nvm")


@pytest.fixture
def shell(home) -> Callable[[str], list[str]]:
    """shell(commands) sources nvm.sh in zsh, runs commands, returns PATH entries."""

    def shell(commands: str = "") -> list[str]:
        script = f'source {NVM_SH}\n{commands}\nprint -r -- "$PATH"'
        result = subprocess.run(
            ["zsh", "--no-rcs", "-c", script],
            env={"HOME": str(home), "PATH": "/usr/bin:/bin"},
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip().split(":")

    return shell


@pytest.mark.parametrize(
    ("default", "installed", "expected"),
    [
        ("node", ["v9.0.0", "v22.17.0", "v20.1.0"], "v22.17.0"),
        ("22", ["v22.2.0", "v22.17.0", "v24.1.0"], "v22.17.0"),
        ("v22", ["v22.2.0", "v22.17.0", "v24.1.0"], "v22.17.0"),
        ("2", ["v2.5.0", "v22.0.0"], "v2.5.0"),
        ("20.1", ["v20.1.3", "v20.10.0"], "v20.1.3"),
        ("v20.1.0", ["v20.1.0", "v20.10.0"], "v20.1.0"),
    ],
)
def test_default_version_on_path_without_loading_nvm(nvm, shell, default, installed, expected):
    nvm.install(*installed)
    nvm.set_default(default)

    path = shell()

    assert path[0] == nvm.bin(expected)
    assert nvm.calls() == []


@pytest.mark.parametrize(
    ("default", "installed"),
    [
        ("lts/*", ["v22.17.0"]),
        ("18", ["v22.17.0"]),
        (None, ["v22.17.0"]),
    ],
)
def test_unresolved_default_loads_nvm_at_startup(nvm, shell, default, installed):
    nvm.install(*installed)
    if default:
        nvm.set_default(default)

    path = shell()

    assert path == ["/usr/bin", "/bin"]
    assert nvm.calls() == ["sourced "]


def test_first_nvm_call_loads_nvm_without_switching_version(nvm, shell):
    nvm.install("v22.17.0")
    nvm.set_default("node")

    path = shell("nvm ls\nnvm current")

    assert path[0] == nvm.bin("v22.17.0")
    assert nvm.calls() == ["sourced --no-use", "nvm ls", "nvm current"]
