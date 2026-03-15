from src.domain.models.ship import CargoHold, Ship


class ShipPersistenceMapper:
    @staticmethod
    def to_document(ship: Ship) -> dict:
        return {
            "name": ship.name,
            "manufacturer": ship.manufacturer,
            "cargo_holds": [
                {"name": h.name, "volume_scu": h.volume_scu, "max_box_size_scu": h.max_box_size_scu}
                for h in ship.cargo_holds
            ],
            "total_scu": ship.total_scu,
            "scm_speed": ship.scm_speed,
            "quantum_speed": ship.quantum_speed,
            "landing_time_seconds": ship.landing_time_seconds,
            "loading_time_per_scu_seconds": ship.loading_time_per_scu_seconds,
        }

    @staticmethod
    def to_domain(doc: dict) -> Ship:
        return Ship(
            id=str(doc["_id"]),
            name=doc.get("name", ""),
            manufacturer=doc.get("manufacturer", ""),
            cargo_holds=[
                CargoHold(
                    name=h["name"],
                    volume_scu=h["volume_scu"],
                    max_box_size_scu=h["max_box_size_scu"],
                )
                for h in doc.get("cargo_holds", [])
            ],
            total_scu=doc.get("total_scu", 0.0),
            scm_speed=doc.get("scm_speed", 0.0),
            quantum_speed=doc.get("quantum_speed", 0.0),
            landing_time_seconds=doc.get("landing_time_seconds", 0.0),
            loading_time_per_scu_seconds=doc.get("loading_time_per_scu_seconds", 0.0),
        )
