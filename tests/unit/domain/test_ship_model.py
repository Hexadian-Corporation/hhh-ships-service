import dataclasses

import pytest

from src.domain.models.ship import CargoHold, Ship


class TestCargoHoldModel:
    def test_cargo_hold_has_name_and_volume_scu(self) -> None:
        hold = CargoHold(name="Main Hold", volume_scu=96.0)

        assert hold.name == "Main Hold"
        assert hold.volume_scu == 96.0

    def test_cargo_hold_does_not_have_max_box_size_scu(self) -> None:
        fields = {f.name for f in dataclasses.fields(CargoHold)}

        assert "max_box_size_scu" not in fields

    def test_cargo_hold_requires_name(self) -> None:
        with pytest.raises(TypeError):
            CargoHold(volume_scu=96.0)  # type: ignore[call-arg]

    def test_cargo_hold_requires_volume_scu(self) -> None:
        with pytest.raises(TypeError):
            CargoHold(name="Main Hold")  # type: ignore[call-arg]


class TestShipModel:
    def test_ship_defaults(self) -> None:
        ship = Ship()

        assert ship.id is None
        assert ship.name == ""
        assert ship.manufacturer == ""
        assert ship.cargo_holds == []
        assert ship.total_scu == 0.0
        assert ship.scm_speed == 0.0
        assert ship.quantum_speed == 0.0
        assert ship.landing_time_seconds == 0.0
        assert ship.loading_time_per_scu_seconds == 0.0
        assert ship.in_game is True

    def test_ship_fields(self) -> None:
        hold = CargoHold(name="Main Hold", volume_scu=96.0)
        ship = Ship(
            id="abc123",
            name="Zeus MK-2 CL",
            manufacturer="RSI",
            cargo_holds=[hold],
            total_scu=96.0,
            scm_speed=210.0,
            quantum_speed=283_046_000.0,
            landing_time_seconds=120.0,
            loading_time_per_scu_seconds=3.0,
            in_game=False,
        )

        assert ship.id == "abc123"
        assert ship.name == "Zeus MK-2 CL"
        assert ship.manufacturer == "RSI"
        assert ship.cargo_holds == [hold]
        assert ship.total_scu == 96.0
        assert ship.scm_speed == 210.0
        assert ship.quantum_speed == 283_046_000.0
        assert ship.landing_time_seconds == 120.0
        assert ship.loading_time_per_scu_seconds == 3.0
        assert ship.in_game is False

    def test_ship_cargo_holds_default_is_independent(self) -> None:
        ship_a = Ship()
        ship_b = Ship()

        ship_a.cargo_holds.append(CargoHold(name="Hold", volume_scu=10.0))

        assert ship_b.cargo_holds == []
