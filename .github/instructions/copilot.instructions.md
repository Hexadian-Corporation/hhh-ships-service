<critical>Note: This is a living document and will be updated as we refine our processes. Always refer back to this for the latest guidelines. Update whenever necessary. Anytime you discover a new bug or issue, document it here to maintain a comprehensive history.</critical>

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
- **CargoHold** — `name`, `volume_scu`, `max_box_size_scu` (all required, no defaults)

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

## Tooling

| Tool | Command |
|------|---------|
| Run tests | `uv run pytest` |
| Lint | `uv run --with ruff ruff check .` |
| Format | `uv run --with ruff ruff format .` |
