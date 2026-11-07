---
paths:
  - "**/*.py"
  - "**/*.pyi"
  - "**/pyproject.toml"
---

# Python

## Style

- Follow PEP 8, with lines of at most 100 characters.
- Lint and format with ruff. Before calling the work done, run `ruff check --fix` and `ruff format` on the files you changed, and fix what remains.
- A repository without ruff config gets one in `pyproject.toml`, created if missing: `line-length = 100` under `[tool.ruff]` and `extend-select = ["E", "W"]` under `[tool.ruff.lint]`. Python scripts without a `.py` extension go in `extend-include`.

## Types

- Annotate every function signature, with the built-in generics and `X | None` (`list[str]`, not `List[str]` or `Optional`).
- Avoid `Any` except at boundaries such as parsed JSON.
- Use frozen dataclasses for structured data, rather than dicts or tuples passed around.

## Idioms

- Use `pathlib` over `os.path`.
- Manage resources with context managers.
- Call `subprocess.run` with a list of arguments, never `shell=True`, and pass `check` explicitly.
- Use `logging` in library code; scripts may `print`.
- Format strings with f-strings, not `.format()` or `%`.
- Use classes for data or objects with several methods. Keep standalone functions at module level rather than grouping them in a class.

## Tests

- Use pytest, with plain test functions; no test classes.
- Mock only external HTTP APIs, e.g. with `responses`. Otherwise prefer integration-style tests that run the real code paths.
- Do test setup with fixtures, shared ones in `conftest.py`. Fixtures return bound callables, e.g. `git(cwd, *args)` rather than `git(env, cwd, *args)`, and small fake objects, e.g. `gh.fail_checks()` rather than writing to state files.
- Use `pytest.mark.parametrize` instead of loops over cases, so each case reports on its own.
- Fake external CLIs with scripts in `tests/bin`, put first on `PATH`.

## Tooling

- Use uv for environments, dependencies and tools (`uv run`, `uv add`, `uv tool install`); never pip or pipx.
- Declare dependencies in `pyproject.toml`, test tools such as pytest in the `dev` group (`uv add --dev pytest`), and commit `uv.lock`. Run tests with `uv run pytest`.

## Django

- Use Django REST Framework ViewSets. Keep views short; move logic to a `lib.py` file or `lib/` package in the app.
- Compute in the database with queryset annotations and aggregations rather than in Python.
