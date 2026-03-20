from src.domain.models.ship import CargoHold, Ship
from src.infrastructure.adapters.inbound.api.ship_api_mapper import ShipApiMapper
from src.infrastructure.adapters.inbound.api.ship_dto import CargoHoldUpdateDTO, ShipUpdateDTO


def _make_ship() -> Ship:
    return Ship(
        id="abc123",
        name="Aurora",
        manufacturer="RSI",
        cargo_holds=[CargoHold(name="Main", volume_scu=10.0)],
        total_scu=10.0,
        scm_speed=200.0,
        quantum_speed=500.0,
        landing_time_seconds=60.0,
        loading_time_per_scu_seconds=5.0,
        in_game=True,
    )


class TestUpdateToDomain:
    def test_no_updates_returns_same_ship(self) -> None:
        existing = _make_ship()
        dto = ShipUpdateDTO()

        result = ShipApiMapper.update_to_domain(existing, dto)

        assert result is existing

    def test_updates_name(self) -> None:
        existing = _make_ship()
        dto = ShipUpdateDTO(name="Aurora MR")

        result = ShipApiMapper.update_to_domain(existing, dto)

        assert result.name == "Aurora MR"
        assert result.manufacturer == existing.manufacturer

    def test_updates_manufacturer(self) -> None:
        existing = _make_ship()
        dto = ShipUpdateDTO(manufacturer="Aegis")

        result = ShipApiMapper.update_to_domain(existing, dto)

        assert result.manufacturer == "Aegis"
        assert result.name == existing.name

    def test_updates_cargo_holds(self) -> None:
        existing = _make_ship()
        dto = ShipUpdateDTO(cargo_holds=[CargoHoldUpdateDTO(name="Cargo Bay", volume_scu=50.0)])

        result = ShipApiMapper.update_to_domain(existing, dto)

        assert len(result.cargo_holds) == 1
        assert result.cargo_holds[0].name == "Cargo Bay"
        assert result.cargo_holds[0].volume_scu == 50.0

    def test_updates_total_scu(self) -> None:
        existing = _make_ship()
        dto = ShipUpdateDTO(total_scu=100.0)

        result = ShipApiMapper.update_to_domain(existing, dto)

        assert result.total_scu == 100.0

    def test_updates_scm_speed(self) -> None:
        existing = _make_ship()
        dto = ShipUpdateDTO(scm_speed=300.0)

        result = ShipApiMapper.update_to_domain(existing, dto)

        assert result.scm_speed == 300.0

    def test_updates_quantum_speed(self) -> None:
        existing = _make_ship()
        dto = ShipUpdateDTO(quantum_speed=800.0)

        result = ShipApiMapper.update_to_domain(existing, dto)

        assert result.quantum_speed == 800.0

    def test_updates_landing_time_seconds(self) -> None:
        existing = _make_ship()
        dto = ShipUpdateDTO(landing_time_seconds=90.0)

        result = ShipApiMapper.update_to_domain(existing, dto)

        assert result.landing_time_seconds == 90.0

    def test_updates_loading_time_per_scu_seconds(self) -> None:
        existing = _make_ship()
        dto = ShipUpdateDTO(loading_time_per_scu_seconds=3.0)

        result = ShipApiMapper.update_to_domain(existing, dto)

        assert result.loading_time_per_scu_seconds == 3.0

    def test_updates_in_game(self) -> None:
        existing = _make_ship()
        dto = ShipUpdateDTO(in_game=False)

        result = ShipApiMapper.update_to_domain(existing, dto)

        assert result.in_game is False

    def test_updates_multiple_fields(self) -> None:
        existing = _make_ship()
        dto = ShipUpdateDTO(name="Zeus", manufacturer="MISC", total_scu=200.0)

        result = ShipApiMapper.update_to_domain(existing, dto)

        assert result.name == "Zeus"
        assert result.manufacturer == "MISC"
        assert result.total_scu == 200.0
        assert result.scm_speed == existing.scm_speed
