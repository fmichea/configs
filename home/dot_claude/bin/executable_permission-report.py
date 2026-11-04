#!/usr/bin/env python3
"""Summarize the permission prompts logged by ~/.claude/hooks/permission-log.sh.

Groups prompts by the allow rule Claude Code suggested for them and prints the
most frequent first, as candidates for permissions.allow in settings.json.
"""

import argparse
import json
import os
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_LOG = Path.home() / ".claude" / "permission-log.jsonl"
EXAMPLE_WIDTH = 70


@dataclass
class RuleStats:
    count: int = 0
    projects: set[str] = field(default_factory=set)
    example: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--log",
        type=Path,
        default=Path(os.environ.get("CLAUDE_PERMISSION_LOG", DEFAULT_LOG)),
        help="JSONL log written by permission-log.sh",
    )
    parser.add_argument(
        "--since-days",
        type=int,
        help="only count prompts from the last N days",
    )
    parser.add_argument(
        "--min-count",
        type=int,
        default=1,
        help="hide rules seen fewer than N times",
    )
    return parser.parse_args()


def read_entries(log: Path) -> list[dict]:
    entries = []
    for line in log.read_text().splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def is_recent(entry: dict, cutoff: datetime | None) -> bool:
    if cutoff is None:
        return True
    try:
        return datetime.fromisoformat(entry["ts"]) >= cutoff
    except (KeyError, ValueError):
        return False


def summarize_input(entry: dict) -> str:
    tool_input = entry.get("tool_input") or {}
    for key in ("command", "file_path", "url", "path"):
        if key in tool_input:
            return " ".join(str(tool_input[key]).split())
    return json.dumps(tool_input, sort_keys=True)


def format_rule(rule: dict) -> str:
    content = rule.get("ruleContent")
    if content:
        return f"{rule['toolName']}({content})"
    return rule["toolName"]


def suggested_rules(entry: dict) -> list[str]:
    rules = []
    for suggestion in entry.get("permission_suggestions") or []:
        if suggestion.get("type") == "addRules" and suggestion.get("behavior") == "allow":
            rules.extend(format_rule(rule) for rule in suggestion.get("rules", []))
    return rules


def rules_for(entry: dict) -> list[str]:
    rules = suggested_rules(entry)
    if rules:
        return rules
    summary = truncate(summarize_input(entry), EXAMPLE_WIDTH)
    return [f"{entry.get('tool_name', '?')} [no suggestion] {summary}"]


def truncate(text: str, width: int) -> str:
    if len(text) <= width:
        return text
    return text[: width - 1] + "…"


def aggregate(entries: list[dict]) -> dict[str, RuleStats]:
    stats: dict[str, RuleStats] = defaultdict(RuleStats)
    for entry in entries:
        for rule in rules_for(entry):
            rule_stats = stats[rule]
            rule_stats.count += 1
            rule_stats.projects.add(entry.get("cwd", "?"))
            rule_stats.example = truncate(summarize_input(entry), EXAMPLE_WIDTH)
    return stats


def print_report(stats: dict[str, RuleStats], min_count: int) -> None:
    rows = [(rule, s) for rule, s in stats.items() if s.count >= min_count]
    if not rows:
        print("No permission prompts logged.")
        return
    rows.sort(key=lambda row: (-row[1].count, row[0]))
    print(f"{'count':>5}  {'dirs':>4}  rule")
    for rule, s in rows:
        print(f"{s.count:>5}  {len(s.projects):>4}  {rule}")
        print(f"{'':>13}e.g. {s.example}")


def main() -> None:
    args = parse_args()
    if not args.log.exists():
        print(f"No log at {args.log}.")
        return
    cutoff = None
    if args.since_days is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=args.since_days)
    entries = [e for e in read_entries(args.log) if is_recent(e, cutoff)]
    print_report(aggregate(entries), args.min_count)


if __name__ == "__main__":
    main()
