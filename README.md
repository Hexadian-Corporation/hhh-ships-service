# hhh-ships-service

Ship specifications and cargo capacity management microservice for **H³ – Hexadian Hauling Helper**.

## Domain

Manages ship data including cargo holds, SCU capacity, SCM/quantum speeds, and loading times.

## Stack

- Python 3.11+ / FastAPI
- MongoDB (database: `hhh_ships`)
- opyoid (dependency injection)
- Hexagonal architecture (Ports & Adapters)

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- MongoDB running on localhost:27017

## Setup

```bash
uv sync
```

## Run

```bash
uv run uvicorn src.main:app --reload --port 8002
```

## Test

```bash
uv run pytest
```

## Lint

```bash
uv run ruff check .
```

## Format

```bash
uv run ruff format .
```

## Run in Docker (full stack)

From the monorepo root (`hexadian-hauling-helper`):

```bash
uv run hhh up
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `HHH_SHIPS_MONGO_URI` | `mongodb://localhost:27017` | MongoDB connection string |
| `HHH_SHIPS_MONGO_DB` | `hhh_ships` | Database name |
| `HHH_SHIPS_PORT` | `8002` | Service port |
| `HEXADIAN_AUTH_JWT_SECRET` | `change-me-in-production` | Shared secret key for JWT signature verification |
| `HHH_SHIPS_JWT_ALGORITHM` | `HS256` | JWT signing algorithm |

## API

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| `POST` | `/ships/` | `hhh:ships:write` | Create a ship |
| `GET` | `/ships/{id}` | `hhh:ships:read` | Get ship by ID |
| `GET` | `/ships/` | `hhh:ships:read` | List all ships |
| `DELETE` | `/ships/{id}` | `hhh:ships:delete` | Delete a ship |
| `GET` | `/health` | Public | Health check |
