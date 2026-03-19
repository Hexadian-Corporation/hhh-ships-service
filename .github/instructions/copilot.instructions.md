<critical>Note: This is a living document and will be updated as we refine our processes. Always refer back to this for the latest guidelines. Update whenever necessary.</critical>

<critical>**Development Workflow:** All changes go through a branch + PR — no direct commits to `main` unless explicitly instructed. See `.github/instructions/development-workflow.instructions.md`.</critical>

<critical>**PR and Issue linkage:** When creating a pull request from an issue, always mention the issue number in the PR description using `Fixes #N`, `Closes #N`, or `Resolves #N`. This is required for GitHub to auto-close the issue on merge.</critical>

<critical>**Before starting implementation:** Read ALL instruction files in `.github/instructions/` of this repository. Also read the organization-level instructions from the `Hexadian-Corporation/.github` repository (`.github/instructions/` directory). These contain essential rules for workflow, bug history, domain models, and GitHub procedures that you MUST follow.</critical>

<critical>**PR title:** The PR title MUST be identical to the originating issue title. Set the final PR title (remove the `[WIP]` prefix) before beginning implementation, not after.</critical>

# Copilot Instructions — hhh-ships-service

## Project Context

**H³ (Hexadian Hauling Helper)** is a Star Citizen companion app for managing hauling contracts, owned by **Hexadian Corporation** (GitHub org: `Hexadian-Corporation`).

This service manages **ship data** — cargo capacity, speed, and other specs used by the route optimizer.

- **Repo:** `Hexadian-Corporation/hhh-ships-service`
- **Port:** 8002
- **Stack:** Python · FastAPI · MongoDB · pymongo · opyoid (DI) · pydantic-settings

## Architecture — Hexagonal (Ports & Adapters)

```
src/
├── main.py                          # FastAPI app factory + uvicorn
├── domain/
│   ├── models/                      # Pure dataclasses (no framework deps)
│   └── exceptions/                  # Domain-specific exceptions
├── application/
│   ├── ports/
│   │   ├── inbound/                 # Service interfaces (ABC)
│   │   └── outbound/               # Repository interfaces (ABC)
│   └── services/                    # Implementations of inbound ports
└── infrastructure/
    ├── config/
    │   ├── settings.py              # pydantic-settings (env prefix: HHH_SHIPS_)
    │   └── dependencies.py          # opyoid DI Module
    └── adapters/
        ├── inbound/api/             # FastAPI router, DTOs (Pydantic), API mappers
        └── outbound/persistence/    # MongoDB repository, persistence mappers
```

**Key conventions:**
- Domain models are **pure Python dataclasses** — no Pydantic, no ORM
- DTOs at the API boundary are **Pydantic BaseModel** subclasses
- Mappers are **static classes** (`to_domain`, `to_dto`, `to_document`)
- DI uses **opyoid** (`Module`, `Injector`, `SingletonScope`)
- Repositories use **pymongo** directly (no ODM)
- Router pattern: **`init_router(service)` + module-level `router`** (standard pattern)

## Domain Model

- **Ship** — `id`, `name`, `manufacturer`, `cargo_holds` (list), `total_scu`, `scm_speed`, `quantum_speed`, `landing_time_seconds`, `loading_time_per_scu_seconds`
- **CargoHold** — `name`, `volume_scu` (all required, no defaults)

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `HHH_SHIPS_MONGO_URI` | `mongodb://localhost:27017` | MongoDB connection string |
| `HHH_SHIPS_MONGO_DB` | `hhh_ships` | Database name |
| `HHH_SHIPS_PORT` | `8002` | Service port |

## API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ships/` | Create a ship |
| `GET` | `/ships/{id}` | Get ship by ID |
| `GET` | `/ships/` | List all ships |
| `DELETE` | `/ships/{id}` | Delete a ship |
| `GET` | `/health` | Health check |

## Issue & PR Title Format

**Format:** `<type>(ships): description`

- Example: `feat(ships): add ship CRUD`
- Example: `fix(ships): correct cargo hold validation`

**Allowed types:** `chore`, `fix`, `ci`, `docs`, `feat`, `refactor`, `test`, `build`, `perf`, `style`, `revert`

The issue title and PR title must be **identical**. PR body must include `Fixes #N`.

## Quality Standards

- `ruff check .` + `ruff format --check .` must pass
- `pytest --cov=src` with ≥90% coverage on changed lines (`diff-cover`)
- Type hints on all functions
- Squash merge only — PR title becomes the commit message

## CI & Branch Protection

**Required status checks** (all with `app_id: 15368` — GitHub Actions):
- `Lint & Format` — `ruff check .` + `ruff format --check .`
- `Tests & Coverage` — `pytest` + `diff-cover` (≥90% on changed lines)
- `Validate PR Title` — conventional commit format
- `Secret Scan` — gitleaks

> **Critical:** Required status checks must always use `app_id: 15368` (GitHub Actions). Using `app_id: null` causes checks to freeze as "Expected — Waiting for status" for any check name not previously reported on `main`. See BUG-011.

## Tooling

| Action | Command |
|--------|---------|
| Setup | `uv sync` |
| Run (dev) | `uv run uvicorn src.main:app --reload --port 8002` |
| Run in Docker | `uv run hhh up` (from monorepo root) |
| Test | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |

## Maintenance Rules

- **Keep the README up to date.** When you add, remove, or change commands, environment variables, API endpoints, domain models, or architecture — update `README.md`. The README is the source of truth for developers.
- **Keep the monorepo CLI service registry up to date.** When adding or removing a service, update `SERVICES`, `FRONTENDS`, `COMPOSE_SERVICE_MAP`, and `SERVICE_ALIASES` in `hexadian-hauling-helper/hhh_cli/__init__.py`, plus the `docker-compose.yml` entry.

## Organization Profile Maintenance

- **Keep the org profile README up to date.** When repositories, ports, architecture, workflows, security policy, or ownership change, update Hexadian-Corporation/.github/profile/README.md in the public .github repo.
- **Treat the org profile as canonical org summary.** Ensure descriptions in this repo remain consistent with the organization profile README.

Remember, before finishing: resolve any merge conflict and merge source (PR origin and destination) branch into current one.