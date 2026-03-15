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

From the monorepo root (`hhh-main`):

```bash
uv run hhh up
```

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
