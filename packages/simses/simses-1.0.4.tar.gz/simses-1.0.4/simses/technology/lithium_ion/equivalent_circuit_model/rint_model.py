from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.technology.lithium_ion.cell.type import CellType
from simses.technology.lithium_ion.equivalent_circuit_model.equivalent_circuit import EquivalentCircuitModel


class RintModel(EquivalentCircuitModel):

    def __init__(self, cell_type: CellType):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__cell_type: CellType = cell_type

    def update(self, time: float, battery_state: LithiumIonState) -> None:
        cell: CellType = self.__cell_type
        bs: LithiumIonState = battery_state
        self.__update_soc(time, bs, cell)
        ocv: float = cell.get_open_circuit_voltage(bs)  # V
        bs.voltage_open_circuit = ocv
        rint: float = bs.internal_resistance
        bs.voltage = ocv + rint * bs.current
        bs.power_loss = rint * bs.current ** 2

    def __update_soc(self, time: float, bs: LithiumIonState, cell: CellType) -> None:
        coulomb_eff = cell.get_coulomb_efficiency(bs)
        self_discharge_rate: float = cell.get_self_discharge_rate() * (time - bs.time)
        # Ah (better As) counting
        denergy: float = bs.current * bs.voltage_open_circuit * (time - bs.time) / 3600.0 * coulomb_eff
        dsoc: float = denergy / bs.capacity - self_discharge_rate
        self.__log.debug('Delta SOC: ' + str(dsoc))
        bs.soc += dsoc
        if 0.0 < bs.soc < 1e-7:
            self.__log.warn('SOC was tried to be set to a value of ' + str(bs.soc) + ' but adjusted to 0.')
            bs.soc = 0.0

    def close(self) -> None:
        self.__log.close()
