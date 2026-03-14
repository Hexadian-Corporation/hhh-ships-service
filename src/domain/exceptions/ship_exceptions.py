class ShipNotFoundError(Exception):
    def __init__(self, ship_id: str) -> None:
        super().__init__(f"Ship not found: {ship_id}")
        self.ship_id = ship_id
