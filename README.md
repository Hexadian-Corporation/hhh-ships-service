# hhh-ships-service

Ship specifications and cargo capacity management microservice for **H³ – Hexadian Hauling Helper**.

## Domain

Manages ship data including cargo holds, SCU capacity, SCM/quantum speeds, and loading times.

## Stack

- Python 3.11+ / FastAPI
- MongoDB (database: `hhh_ships`)
- opyoid (dependency injection)
- Hexagonal architecture (Ports & Adapters)

## Quick Start

```bash
uv sync
uv run uvicorn src.main:app --reload --port 8002
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
