from configparser import ConfigParser

from simses.commons.data.data_handler import DataHandler
from simses.commons.state.abstract_state import State
from simses.commons.state.parameters import SystemParameters
from simses.commons.state.system import SystemState
from simses.logic.power_distribution.power_distributor import PowerDistributor
from simses.system.factory import StorageSystemFactory
from simses.system.storage_system_ac import StorageSystemAC


class StorageCircuit:

    """
    StorageCircuit is the top level class including all AC storage systems. The is distributed via a PowerDistributor
    logic to each AC storage system.
    """

    def __init__(self, data_export: DataHandler, config: ConfigParser):
        factory: StorageSystemFactory = StorageSystemFactory(config)
        self.__storage_systems: [StorageSystemAC] = factory.create_storage_systems_ac(data_export)
        self.__power_distributor: PowerDistributor = factory.create_power_distributor_ac()
        # for system in self.__storage_systems:
        #     self.__power_distributor.set_max_system_power_for(system.system_id, system.max_power)
        factory.close()

    def update(self, time: float, power: float) -> None:
        states: [State] = list()
        for system in self.__storage_systems:
            states.append(system.state)
        self.__power_distributor.set(time, states)
        for system in self.__storage_systems:
            local_power: float = self.__power_distributor.get_power_for(power, system.state)
            system.update(local_power, time)

    @property
    def state(self) -> SystemState:
        system_states = list()
        for storage in self.__storage_systems:
            system_states.append(storage.state)
        system_state: SystemState = SystemState.sum_parallel(system_states)
        system_state.set(SystemState.SYSTEM_AC_ID, 0)
        system_state.set(SystemState.SYSTEM_DC_ID, 0)
        return system_state

    def get_system_parameters(self) -> dict:
        parameters: dict = dict()
        subsystems: list = list()
        for system in self.__storage_systems:
            subsystems.append(system.get_system_parameters())
        parameters[SystemParameters.POWER_DISTRIBUTION] = type(self.__power_distributor).__name__
        parameters[SystemParameters.SUBSYSTEM] = subsystems
        return {SystemParameters.PARAMETERS: parameters}

    def close(self) -> None:
        """Closing all resources in storage systems"""
        self.__power_distributor.close()
        for storage in self.__storage_systems:
            storage.close()
