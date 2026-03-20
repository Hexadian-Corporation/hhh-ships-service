from fastapi.testclient import TestClient

from tests.auth_helpers import make_auth_header

_READ = make_auth_header("hhh:ships:read")
_WRITE = make_auth_header("hhh:ships:write")
_DELETE = make_auth_header("hhh:ships:delete")
_ALL = make_auth_header("hhh:ships:read", "hhh:ships:write", "hhh:ships:delete")


def _full_ship_payload() -> dict:
    return {
        "name": "Caterpillar",
        "manufacturer": "Drake",
        "cargo_holds": [
            {"name": "Module 1", "volume_scu": 144.0},
            {"name": "Module 2", "volume_scu": 144.0},
        ],
        "total_scu": 288.0,
        "scm_speed": 150.0,
        "quantum_speed": 283_046_000.0,
        "landing_time_seconds": 90.0,
        "loading_time_per_scu_seconds": 3.0,
        "in_game": True,
    }


def _minimal_ship_payload() -> dict:
    return {"name": "Aurora", "manufacturer": "RSI"}


def _create_ship(client: TestClient, payload: dict | None = None) -> dict:
    resp = client.post("/ships/", json=payload or _full_ship_payload(), headers=_ALL)
    assert resp.status_code == 201
    return resp.json()


# ---------- POST /ships/ ----------


class TestPostShip:
    def test_create_ship_with_all_fields(self, client: TestClient) -> None:
        payload = _full_ship_payload()
        resp = client.post("/ships/", json=payload, headers=_ALL)

        assert resp.status_code == 201
        body = resp.json()
        assert body["name"] == payload["name"]
        assert body["manufacturer"] == payload["manufacturer"]
        assert len(body["cargo_holds"]) == 2
        assert body["cargo_holds"][0]["name"] == "Module 1"
        assert body["cargo_holds"][0]["volume_scu"] == 144.0
        assert body["total_scu"] == 288.0
        assert body["scm_speed"] == 150.0
        assert body["quantum_speed"] == 283_046_000.0
        assert body["landing_time_seconds"] == 90.0
        assert body["loading_time_per_scu_seconds"] == 3.0
        assert body["in_game"] is True

    def test_create_ship_with_minimal_fields(self, client: TestClient) -> None:
        resp = client.post("/ships/", json=_minimal_ship_payload(), headers=_ALL)

        assert resp.status_code == 201
        body = resp.json()
        assert body["name"] == "Aurora"
        assert body["manufacturer"] == "RSI"
        assert body["cargo_holds"] == []
        assert body["total_scu"] == 0.0

    def test_create_ship_with_multiple_cargo_holds(self, client: TestClient) -> None:
        payload = {
            "name": "Hull C",
            "manufacturer": "MISC",
            "cargo_holds": [
                {"name": "Spindle A", "volume_scu": 1000.0},
                {"name": "Spindle B", "volume_scu": 1000.0},
                {"name": "Spindle C", "volume_scu": 1000.0},
            ],
            "total_scu": 3000.0,
        }
        resp = client.post("/ships/", json=payload, headers=_ALL)

        assert resp.status_code == 201
        body = resp.json()
        assert len(body["cargo_holds"]) == 3
        holds = {h["name"] for h in body["cargo_holds"]}
        assert holds == {"Spindle A", "Spindle B", "Spindle C"}

    def test_create_ship_generates_id(self, client: TestClient) -> None:
        body = _create_ship(client)
        assert body["_id"] is not None
        assert isinstance(body["_id"], str)
        assert len(body["_id"]) == 24  # MongoDB ObjectId hex string

    def test_create_ship_returns_201(self, client: TestClient) -> None:
        resp = client.post("/ships/", json=_full_ship_payload(), headers=_ALL)
        assert resp.status_code == 201

    def test_cargo_hold_has_no_max_box_size_scu(self, client: TestClient) -> None:
        body = _create_ship(client)
        for hold in body["cargo_holds"]:
            assert "max_box_size_scu" not in hold


# ---------- GET /ships/ ----------


class TestGetShips:
    def test_list_empty(self, client: TestClient) -> None:
        resp = client.get("/ships/", headers=_READ)

        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_multiple_ships(self, client: TestClient) -> None:
        _create_ship(client, {"name": "Aurora", "manufacturer": "RSI"})
        _create_ship(client, {"name": "Freelancer", "manufacturer": "MISC"})

        resp = client.get("/ships/", headers=_READ)

        assert resp.status_code == 200
        ships = resp.json()
        assert len(ships) == 2
        names = {s["name"] for s in ships}
        assert names == {"Aurora", "Freelancer"}

    def test_list_ships_contains_all_fields(self, client: TestClient) -> None:
        _create_ship(client, _full_ship_payload())

        resp = client.get("/ships/", headers=_READ)

        assert resp.status_code == 200
        ship = resp.json()[0]
        assert "_id" in ship
        assert "name" in ship
        assert "manufacturer" in ship
        assert "cargo_holds" in ship
        assert "total_scu" in ship
        assert "scm_speed" in ship
        assert "quantum_speed" in ship
        assert "landing_time_seconds" in ship
        assert "loading_time_per_scu_seconds" in ship
        assert "in_game" in ship


# ---------- GET /ships/{id} ----------


class TestGetShipById:
    def test_get_existing_ship(self, client: TestClient) -> None:
        created = _create_ship(client)
        ship_id = created["_id"]

        resp = client.get(f"/ships/{ship_id}", headers=_READ)

        assert resp.status_code == 200
        body = resp.json()
        assert body["_id"] == ship_id
        assert body["name"] == created["name"]

    def test_get_nonexistent_ship_returns_404(self, client: TestClient) -> None:
        fake_id = "000000000000000000000000"
        resp = client.get(f"/ships/{fake_id}", headers=_READ)

        assert resp.status_code == 404


# ---------- PUT /ships/{id} ----------


class TestPutShip:
    def test_full_update(self, client: TestClient) -> None:
        created = _create_ship(client, _full_ship_payload())
        ship_id = created["_id"]

        update_payload = {
            "name": "Caterpillar Best-In-Show",
            "manufacturer": "Drake Industries",
            "cargo_holds": [{"name": "Single Bay", "volume_scu": 500.0}],
            "total_scu": 500.0,
            "scm_speed": 160.0,
            "quantum_speed": 300_000_000.0,
            "landing_time_seconds": 100.0,
            "loading_time_per_scu_seconds": 4.0,
            "in_game": False,
        }

        resp = client.put(f"/ships/{ship_id}", json=update_payload, headers=_ALL)

        assert resp.status_code == 200
        body = resp.json()
        assert body["name"] == "Caterpillar Best-In-Show"
        assert body["manufacturer"] == "Drake Industries"
        assert len(body["cargo_holds"]) == 1
        assert body["total_scu"] == 500.0
        assert body["scm_speed"] == 160.0
        assert body["quantum_speed"] == 300_000_000.0
        assert body["landing_time_seconds"] == 100.0
        assert body["loading_time_per_scu_seconds"] == 4.0
        assert body["in_game"] is False

    def test_partial_update_name_only(self, client: TestClient) -> None:
        created = _create_ship(client, _full_ship_payload())
        ship_id = created["_id"]

        resp = client.put(f"/ships/{ship_id}", json={"name": "Caterpillar MK2"}, headers=_ALL)

        assert resp.status_code == 200
        body = resp.json()
        assert body["name"] == "Caterpillar MK2"
        assert body["manufacturer"] == created["manufacturer"]
        assert body["total_scu"] == created["total_scu"]

    def test_update_nonexistent_ship_returns_404(self, client: TestClient) -> None:
        fake_id = "000000000000000000000000"
        resp = client.put(f"/ships/{fake_id}", json={"name": "Ghost Ship"}, headers=_ALL)

        assert resp.status_code == 404

    def test_add_cargo_holds_on_update(self, client: TestClient) -> None:
        created = _create_ship(client, _minimal_ship_payload())
        ship_id = created["_id"]
        assert created["cargo_holds"] == []

        update = {
            "cargo_holds": [
                {"name": "Hold A", "volume_scu": 50.0},
                {"name": "Hold B", "volume_scu": 75.0},
            ],
        }
        resp = client.put(f"/ships/{ship_id}", json=update, headers=_ALL)

        assert resp.status_code == 200
        body = resp.json()
        assert len(body["cargo_holds"]) == 2

    def test_remove_cargo_holds_on_update(self, client: TestClient) -> None:
        created = _create_ship(client, _full_ship_payload())
        ship_id = created["_id"]
        assert len(created["cargo_holds"]) == 2

        resp = client.put(f"/ships/{ship_id}", json={"cargo_holds": []}, headers=_ALL)

        assert resp.status_code == 200
        assert resp.json()["cargo_holds"] == []

    def test_update_persists_to_database(self, client: TestClient) -> None:
        created = _create_ship(client, _full_ship_payload())
        ship_id = created["_id"]

        client.put(f"/ships/{ship_id}", json={"name": "Updated Name"}, headers=_ALL)

        resp = client.get(f"/ships/{ship_id}", headers=_READ)
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Name"


# ---------- DELETE /ships/{id} ----------


class TestDeleteShip:
    def test_delete_existing_ship(self, client: TestClient) -> None:
        created = _create_ship(client)
        ship_id = created["_id"]

        resp = client.delete(f"/ships/{ship_id}", headers=_ALL)
        assert resp.status_code == 204

        get_resp = client.get(f"/ships/{ship_id}", headers=_READ)
        assert get_resp.status_code == 404

    def test_delete_nonexistent_ship_returns_404(self, client: TestClient) -> None:
        fake_id = "000000000000000000000000"
        resp = client.delete(f"/ships/{fake_id}", headers=_ALL)

        assert resp.status_code == 404


# ---------- Cache-Control headers ----------


class TestCacheControlHeaders:
    def test_get_ship_has_cache_control(self, client: TestClient) -> None:
        created = _create_ship(client)
        ship_id = created["_id"]

        resp = client.get(f"/ships/{ship_id}", headers=_READ)

        assert resp.status_code == 200
        assert resp.headers["cache-control"] == "max-age=600"

    def test_list_ships_has_cache_control(self, client: TestClient) -> None:
        resp = client.get("/ships/", headers=_READ)

        assert resp.status_code == 200
        assert resp.headers["cache-control"] == "max-age=600"
