from .base import BaseDataSource


class TestingDataSource(BaseDataSource):
    """
    A data source that keeps all data in RAM, and starts off with 0s.

    Analog inputs and discrete inputs are always 0.
    """

    def __init__(self):
        self.holding_registers = {}
        self.coils = {}

    def get_analog_input(self, unit_id: int, address: int) -> int:
        return 0

    def get_discrete_input(self, unit_id: int, address: int) -> bool:
        return False

    def get_holding_register(self, unit_id: int, address: int) -> int:
        return self.holding_registers.get((unit_id, address), 0)

    def get_coil(self, unit_id: int, address: int) -> bool:
        return self.coils.get((unit_id, address), False)

    def set_holding_register(self, unit_id: int, address: int, value: int) -> None:
        self.holding_registers[(unit_id, address)] = value

    def set_coil(self, unit_id: int, address: int, value: bool) -> None:
        self.coils[(unit_id, address)] = value
