# Contributing to Model Diet

Thanks for your interest in improving Model Diet. Contributions should help users profile a fitted model and interpret its results clearly.

## Development setup

Model Diet requires Python 3.11 or later. From the repository root, create and activate a virtual environment, then install the test and demo dependencies in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test,demo]"
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run the test suite

Run the full suite before submitting a change:

```bash
python -m pytest -v
```

Add or update tests when behavior changes. Keep tests independent of live network services and avoid relying on optional frameworks unless the test dependencies explicitly install them.

## Make focused changes

- Keep changes scoped to the behavior being addressed.
- Preserve the documented meaning and units of existing measurements. A change to measurement semantics should update the implementation, tests, and documentation together.
- Use `modeldiet` as the canonical package import path.
- Do not add compatibility imports for obsolete package names.
- Keep profiling results serializable and document custom measurement units and semantics.

## Check documentation and distributions

When changing the public API or its behavior, update the README and add a test or example that demonstrates the change. Verify examples against the installed package when practical.

To build distributions locally:

```bash
python -m pip install build
python -m build
```

## Propose a change

Open an issue first for large changes or new measurement areas so the scope and expected semantics can be discussed. For a pull request, describe the user-visible behavior, note any limitations, and report the checks you ran.
