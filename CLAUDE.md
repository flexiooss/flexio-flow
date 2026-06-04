# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Setup (first time):**
```bash
bash ./venv.sh               # create virtualenv and install dependencies
source $PWD/venv/bin/activate
```

**Run the tool:**
```bash
bash ./flexio-flow.sh <args>  # e.g. bash ./flexio-flow.sh -h
```

**Run all tests:**
```bash
bash ./test.sh
```

**Run a single test module:**
```bash
bash ./test.sh tests.VersionControl.GitFlow.TestGitFlow
```

**Type checking:**
```bash
bash ./mypy.sh
```

**Update pip requirements** (with venv active):
```bash
python3 -m pip freeze > requirements.txt
```

## Architecture

`flexio-flow` is a Python CLI implementing a git branching workflow (gitflow-style) with version management and optional GitHub/Flexio issue tracking.

### Entry point and dispatch

`src/main.py` → `Executor.exec(argv)` → `FlexioFlow.process()`

`Executor` parses CLI args, resolves the working directory (walks up until it finds `flexio-flow.yml`), and builds an `ExecutorConfig` containing:
- `task` (`Task` enum): top-level command — `branch`, `core`, `issue`, `topics`, `version`, `poom-ci`, etc.
- `branch` (`Branches` enum): `develop`, `feature`, `hotfix`, `master`, `release`
- `branch_action` (`Actions` enum): `init`, `start`, `finish`, `commit`, `precheck`
- `options`: parsed CLI flags

`FlexioFlow.process()` then dispatches to the appropriate handler.

### State and configuration

- **`flexio-flow.yml`** (per-repo, in the working directory): managed by `StateHandler`. Contains `version` (semver string), `level` (`dev`|`stable`), `schemes` (list), and `topics` (issue numbers). This is the file that gets committed on every version bump.
- **`~/.flexio-flow/config.yml`**: global user config managed by `ConfigHandler` (`Core.CONFIG_DIR`). Contains GitHub credentials, Flexio credentials, and optional branch name overrides. Initialize with `flexio-flow core config`.

### Git operations

`VersionControl/Git/GitCmd` wraps all `subprocess.Popen` git calls. All branch-level operations live under `VersionControl/Git/Branches/{Feature,Hotfix,Release,Master,Develop}/` with `Start.py` and `Finish.py` classes.

The `GitFlowCmd` helper (in `VersionControl/Git/Branches/GitFlowCmd.py`) handles gitflow-specific queries (e.g. `has_release()`, `is_release()`).

### Branch flow mechanics

A typical `release start` sequence:
1. Check clean working tree and no existing release/hotfix
2. Pull develop and master
3. Bump version in `StateHandler`
4. Create branch `release/X.Y.Z#<topic>` from develop
5. Set level to `stable`, write `flexio-flow.yml`
6. Update scheme files via `UpdateSchemeVersion`
7. Commit and push

A typical `release finish` sequence:
1. Run precheck (scheme dependency checks)
2. Merge release → master with `--no-ff --strategy-option theirs`, tag the version
3. Bump next dev version, write `flexio-flow.yml`, merge release → develop
4. Delete release branch

### Schemes

`Schemes/{Maven,Package,Composer}` update version numbers in scheme-specific files (`pom.xml`, `package.json`, `composer.json`). `SchemeBuilder.create()` instantiates the right one. `UpdateSchemeVersion.from_state_handler()` applies all configured schemes at once.

### Version control providers

`VersionControlProvider/Github/` and `VersionControlProvider/Flexio/` handle API calls for issue and topic management. GitHub is used as the "issuer" (for issues/milestones); Flexio is used as the "topicer" (for topics). Both are optional — only active when `activate: true` in the global config.

### PoomCi

`PoomCiDependency/` generates a JSON dependency graph for CI systems (`flexio-flow poom ci full-repository-json`).

### Tests

Tests live under `src/tests/`. The test runner must be invoked from inside `src/` (handled by `test.sh`). Note that `src/tests/tests.py` has most test suites commented out — individual test modules can be run directly.
