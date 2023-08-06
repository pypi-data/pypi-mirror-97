from simses.commons.profile.power.power_profile import PowerProfile
from simses.commons.config.simulation.energy_management import EnergyManagementConfig
from simses.commons.state.energy_management import EnergyManagementState
from simses.commons.state.system import SystemState
from simses.logic.energy_management.strategy.operation_priority import OperationPriority
from simses.logic.energy_management.strategy.operation_strategy import OperationStrategy


class SimplePeakShaving(OperationStrategy):
    """
    Basic Peak Shaving operation strategy: If the storage is almost full (> xy %),
    the storage is not charged anymore to avoid a misrepresent fulfillmentfactor
    """

    def __init__(self, power_profile: PowerProfile, ems_config: EnergyManagementConfig):
        super().__init__(OperationPriority.VERY_HIGH)
        self.__load_profile: PowerProfile = power_profile
        self.__max_power: float = ems_config.max_power
        self.__power: float = 0.0
        self.__soc_threshold: float = 0.9999
        self.__power_threshold: float = 0.0

    def next(self, time: float, system_state: SystemState, power_offset: float = 0) -> float:
        self.__power = self.__load_profile.next(time)
        net_power = self.__max_power - (self.__power + power_offset)
        if net_power < 0.0:
            return net_power
        elif system_state.soc < self.__soc_threshold and net_power > self.__power_threshold:
            return net_power
        else:
            return 0.0

    def update(self, energy_management_state: EnergyManagementState) -> None:
        energy_management_state.load_power = self.__power
        energy_management_state.peakshaving_limit = self.__max_power

    def clear(self) -> None:
        self.__power = 0.0

    def close(self) -> None:
        self.__load_profile.close()
