from simses.commons.profile.power.power_profile import PowerProfile
from simses.commons.config.simulation.energy_management import EnergyManagementConfig
from simses.commons.state.energy_management import EnergyManagementState
from simses.commons.state.system import SystemState
from simses.logic.energy_management.strategy.operation_priority import OperationPriority
from simses.logic.energy_management.strategy.operation_strategy import OperationStrategy


class EvChargerWithBuffer(OperationStrategy):

    def __init__(self, power_profile: PowerProfile, ems_config: EnergyManagementConfig):
        super().__init__(OperationPriority.MEDIUM)
        self.__load_profile: PowerProfile = power_profile
        self.__max_power: float = ems_config.max_power
        self.__ac_grid = 16000  # AC Power from grid 16kW
        self.__power: float = 0.0
        self.__soc_threshold: float = 0.98
        self.__power_threshold: float = 50.0

    def next(self, time: float, system_state: SystemState, power: float = 0) -> float:
        self.__power = self.__load_profile.next(time)
        # Battery_power = EV_charger_power - AC_input_power_from_grid
        if system_state.soc > 0 or system_state.soc < self.__soc_threshold:
            return self.__ac_grid - self.__power
        else:
            return 0

    def update(self, energy_management_state: EnergyManagementState) -> None:
        energy_management_state.load_power = self.__power

    def clear(self) -> None:
        self.__power = 0.0

    def close(self) -> None:
        self.__load_profile.close()
