import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

DOT_CLAUDE = Path(__file__).resolve().parent.parent / "home" / "dot_claude"
HOOK = DOT_CLAUDE / "hooks" / "executable_permission-log.sh"
REPORT = DOT_CLAUDE / "bin" / "executable_permission-report.py"
HOOK_PATH = "/opt/homebrew/bin:/usr/bin:/bin"


def hook_env(log: Path) -> dict:
    return {"CLAUDE_PERMISSION_LOG": str(log), "PATH": HOOK_PATH}


def bash_request(command: str, rule: str | None, cwd: str = "/repo") -> dict:
    request = {
        "cwd": cwd,
        "hook_event_name": "PermissionRequest",
        "tool_name": "Bash",
        "tool_input": {"command": command},
    }
    if rule is not None:
        request["permission_suggestions"] = [
            {
                "type": "addRules",
                "rules": [{"toolName": "Bash", "ruleContent": rule}],
                "behavior": "allow",
                "destination": "localSettings",
            },
        ]
    return request


def run_hook(log: Path, request: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        [HOOK],
        input=json.dumps(request),
        capture_output=True,
        text=True,
        env=hook_env(log),
        check=True,
    )


def run_report(log: Path, *args: str) -> str:
    result = subprocess.run(
        [sys.executable, REPORT, "--log", str(log), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def write_log(log: Path, entries: list[dict]) -> None:
    log.write_text("".join(json.dumps(entry) + "\n" for entry in entries))


def test_hook_appends_request_with_timestamp_and_prints_nothing(tmp_path):
    log = tmp_path / "log.jsonl"
    request = bash_request("make build", "make build")

    result = run_hook(log, request)
    run_hook(log, request)

    assert result.stdout == ""
    lines = log.read_text().splitlines()
    assert len(lines) == 2
    entry = json.loads(lines[0])
    assert entry["tool_input"] == {"command": "make build"}
    assert datetime.fromisoformat(entry["ts"]) <= datetime.now(timezone.utc)


def test_hook_ignores_invalid_input(tmp_path):
    log = tmp_path / "log.jsonl"

    result = subprocess.run(
        [HOOK],
        input="not json",
        capture_output=True,
        text=True,
        env=hook_env(log),
    )

    assert result.returncode == 0
    assert result.stdout == ""


def test_report_ranks_suggested_rules_by_count(tmp_path):
    log = tmp_path / "log.jsonl"
    write_log(
        log,
        [
            bash_request("make test", "make test *", cwd="/a"),
            bash_request("make test -v", "make test *", cwd="/b"),
            bash_request("kubectl get pods", "kubectl get *"),
        ],
    )

    lines = run_report(log).splitlines()

    assert lines[1].split() == ["2", "2", "Bash(make", "test", "*)"]
    assert lines[3].split() == ["1", "1", "Bash(kubectl", "get", "*)"]


@pytest.mark.parametrize(
    ("request_", "expected_rule"),
    [
        (bash_request("make build", "make build"), "Bash(make build)"),
        (
            {
                "tool_name": "mcp__github__get_issue",
                "tool_input": {},
                "permission_suggestions": [
                    {
                        "type": "addRules",
                        "rules": [{"toolName": "mcp__github__get_issue"}],
                        "behavior": "allow",
                    },
                ],
            },
            "mcp__github__get_issue",
        ),
        (
            bash_request("rm -rf build && make", None),
            "Bash [no suggestion] rm -rf build && make",
        ),
    ],
)
def test_report_shows_rule_for_request(tmp_path, request_, expected_rule):
    log = tmp_path / "log.jsonl"
    write_log(log, [request_])

    assert expected_rule in run_report(log)


def test_report_ignores_deny_suggestions(tmp_path):
    log = tmp_path / "log.jsonl"
    request = bash_request("make build", None)
    request["permission_suggestions"] = [
        {
            "type": "addRules",
            "rules": [{"toolName": "Bash", "ruleContent": "make build"}],
            "behavior": "deny",
        },
    ]
    write_log(log, [request])

    assert "Bash(make build)" not in run_report(log)


def test_report_filters_by_age_and_count(tmp_path):
    log = tmp_path / "log.jsonl"
    old = datetime.now(timezone.utc) - timedelta(days=30)
    entries = [
        {"ts": old.isoformat(), **bash_request("make old", "make old")},
        {"ts": datetime.now(timezone.utc).isoformat(), **bash_request("make new", "make new")},
        {"ts": datetime.now(timezone.utc).isoformat(), **bash_request("make new", "make new")},
        {"ts": datetime.now(timezone.utc).isoformat(), **bash_request("make once", "make once")},
    ]
    write_log(log, entries)

    output = run_report(log, "--since-days", "7", "--min-count", "2")

    assert "Bash(make new)" in output
    assert "Bash(make old)" not in output
    assert "Bash(make once)" not in output


def test_report_skips_malformed_lines(tmp_path):
    log = tmp_path / "log.jsonl"
    log.write_text("garbage\n" + json.dumps(bash_request("make build", "make build")) + "\n")

    assert "Bash(make build)" in run_report(log)


def test_report_handles_missing_log(tmp_path):
    assert "No log at" in run_report(tmp_path / "missing.jsonl")
