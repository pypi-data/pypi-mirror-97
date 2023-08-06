from configparser import ConfigParser

from simses.commons.data.data_handler import DataHandler
from simses.commons.log import Logger
from simses.commons.state.parameters import SystemParameters
from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.system.auxiliary.auxiliary import Auxiliary
from simses.technology.lithium_ion.battery_management_system.management_system import BatteryManagementSystem
from simses.technology.lithium_ion.cell.type import CellType
from simses.technology.lithium_ion.degradation.degradation_model import DegradationModel
from simses.technology.lithium_ion.equivalent_circuit_model.equivalent_circuit import EquivalentCircuitModel
from simses.technology.lithium_ion.factory import LithiumIonFactory
from simses.technology.storage import StorageTechnology


class LithiumIonBattery(StorageTechnology):
    """Battery orchestrates its models for lithium_ion management system, degradation and thermal management as well as
    its equivalent circuit"""

    __ACCURACY = 1e-14
    __MAX_LOOPS = 10

    def __init__(self, cell: str, voltage: float, capacity: float, soc: float, soh: float, data_export: DataHandler,
                 temperature: float, storage_id: int, system_id: int, config: ConfigParser):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__factory: LithiumIonFactory = LithiumIonFactory(config)
        cell_type: CellType = self.__factory.create_cell_type(cell, voltage, capacity, soh)
        self.__cell_type: CellType = cell_type
        self.__battery_state: LithiumIonState = self.__factory.create_battery_state_from(system_id,
                                                                                         storage_id,
                                                                                         cell_type,
                                                                                         temperature,
                                                                                         soc)
        self.__degradation_model: DegradationModel = self.__factory.create_degradation_model_from(cell_type,
                                                                                                  self.__battery_state)
        self.__battery_management_system: BatteryManagementSystem = \
            self.__factory.create_battery_management_system_from(cell_type)
        self.__battery_model: EquivalentCircuitModel = self.__factory.create_battery_model_from(cell_type)
        self.__data_export: DataHandler = data_export
        self.__log.debug('created: ' + str(self.__battery_state))
        self.__data_export.transfer_data(self.__battery_state.to_export()) # initial timestep

    def get_equilibrium_state_for(self, time: float, current: float, parallel: bool = False) -> LithiumIonState:
        """Starting update of lithium_ion"""
        bs: LithiumIonState = LithiumIonState(0, 0)
        bs.set_all(self.__battery_state)
        bs.current = current
        # Included loops for simultaneous current and voltage adjustment
        #power_target is necessary for BMS (fulfillmentfactor calculation)
        power_target: float = bs.current * bs.voltage
        if parallel:
            # no need to calculate Equilibrium, because parallel current was analyticaly calculated based on OCV,
            # nonetheless battery management and battery model needs to be updated
            self.__battery_management_system.update(time, bs, power_target)
            if bs.current != current:
                self.__log.error(
                    'Current of a direct parallel battery was limited by the BMS and would therefore disconnect from DC-Link. Results unusable')
            self.__battery_model.update(time, bs)
        else:
            old_bs: LithiumIonState = LithiumIonState(0, 0)
            old_bs.set_all(bs)
            for step in range(self.__MAX_LOOPS):
                bs.set_all(old_bs)
                self.__battery_management_system.update(time, bs, power_target)
                self.__battery_model.update(time, bs)
                bs.current = old_bs.voltage * bs.current / bs.voltage
                if abs(bs.voltage - old_bs.voltage) < self.__ACCURACY:
                    break
                old_bs.current = bs.current
                old_bs.voltage = bs.voltage
        return bs

    def distribute_and_run(self, time: float, current: float, voltage: float):
        bs: LithiumIonState = self.get_equilibrium_state_for(time, current)
        self.__degradation_model.update(time, bs)
        # TODO update battery temp in system thermal model
        bs.time = time
        self.__data_export.transfer_data(bs.to_export())
        self.__battery_state.set_all(bs)

    @property
    def volume(self) -> float:
        return self.__cell_type.get_volume()

    @property
    def mass(self) -> float:
        return self.__cell_type.get_mass()

    @property
    def surface_area(self) -> float:
        return self.__cell_type.get_surface_area()

    @property
    def specific_heat(self) -> float:
        return self.__cell_type.get_specific_heat()

    @property
    def convection_coefficient(self) -> float:
        return self.__cell_type.get_convection_coefficient()

    @property
    def max_voltage(self) -> float:
        return self.__cell_type.get_max_voltage()

    @property
    def min_voltage(self) -> float:
        return self.__cell_type.get_min_voltage()

    @property
    def max_current(self) -> float:
        return self.__cell_type.get_max_current(self.__battery_state)

    @property
    def min_current(self) -> float:
        return self.__cell_type.get_min_current(self.__battery_state)

    @property
    def id(self) -> int:
        return int(self.__battery_state.get(LithiumIonState.SYSTEM_DC_ID))

    def wait(self):
        pass

    def get_auxiliaries(self) -> [Auxiliary]:
        return list()

    @property
    def state(self) -> LithiumIonState:
        return self.__battery_state

    def get_system_parameters(self) -> dict:
        parameters: dict = dict()
        parameters[SystemParameters.CELL_TYPE] = type(self.__cell_type).__name__
        parameters[SystemParameters.NOMINAL_VOLTAGE] = int(self.__cell_type.get_nominal_voltage())
        parameters[SystemParameters.BATTERY_CIRCUIT] = str(self.__cell_type.get_serial_scale()) + 's' + \
                                                       str(self.__cell_type.get_parallel_scale()) + 'p'
        return parameters

    def close(self) -> None:
        """Closing all resources in lithium_ion"""
        self.__battery_management_system.close()
        self.__battery_model.close()
        self.__degradation_model.close()
        self.__factory.close()
        self.__log.close()
