from unittest.mock import MagicMock

import pytest

from src.domain.models.ship import CargoHold, Ship
from src.seed import SHIPS, seed_ships


def _make_ship(ship_id: str = "id1") -> Ship:
    return Ship(
        id=ship_id,
        name="Zeus MK-2 CL",
        manufacturer="RSI",
        cargo_holds=[
            CargoHold(name="Main Hold", volume_scu=96.0),
            CargoHold(name="Secondary Hold", volume_scu=32.0),
        ],
        total_scu=128.0,
        scm_speed=210.0,
        quantum_speed=283_046_000.0,
        landing_time_seconds=120.0,
        loading_time_per_scu_seconds=3.0,
    )


@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock()


class TestSeedData:
    def test_seed_ships_has_expected_count(self) -> None:
        assert len(SHIPS) == 8

    def test_all_ships_have_name_and_manufacturer(self) -> None:
        for ship in SHIPS:
            assert ship.name
            assert ship.manufacturer

    def test_all_ships_have_cargo_holds(self) -> None:
        for ship in SHIPS:
            assert len(ship.cargo_holds) > 0

    def test_total_scu_matches_cargo_holds(self) -> None:
        for ship in SHIPS:
            hold_total = sum(h.volume_scu for h in ship.cargo_holds)
            assert ship.total_scu >= hold_total

    def test_cargo_hold_volumes_positive(self) -> None:
        for ship in SHIPS:
            for hold in ship.cargo_holds:
                assert hold.volume_scu > 0

    def test_zeus_mk2_cl_data(self) -> None:
        zeus = SHIPS[0]

        assert zeus.name == "Zeus MK-2 CL"
        assert zeus.manufacturer == "RSI"
        assert zeus.total_scu == 128.0
        assert zeus.scm_speed == 210.0
        assert zeus.quantum_speed == 283_046_000.0
        assert len(zeus.cargo_holds) == 2
        assert zeus.cargo_holds[0].name == "Main Hold"
        assert zeus.cargo_holds[0].volume_scu == 96.0
        assert zeus.cargo_holds[1].name == "Secondary Hold"
        assert zeus.cargo_holds[1].volume_scu == 32.0


class TestSeedShips:
    def test_creates_ships_when_none_exist(self, mock_service: MagicMock) -> None:
        mock_service.list_all.return_value = []
        mock_service.create.return_value = _make_ship()

        result = seed_ships(mock_service)

        assert len(result) == len(SHIPS)
        assert mock_service.create.call_count == len(SHIPS)

    def test_skips_when_ships_already_exist(self, mock_service: MagicMock) -> None:
        mock_service.list_all.return_value = [_make_ship()]

        result = seed_ships(mock_service)

        assert result == []
        mock_service.create.assert_not_called()

    def test_uses_replace_copy_not_original(self, mock_service: MagicMock) -> None:
        mock_service.list_all.return_value = []
        mock_service.create.return_value = _make_ship()

        seed_ships(mock_service)

        call_arg = mock_service.create.call_args[0][0]
        assert call_arg is not SHIPS[0]
