from simses.commons.config.simulation.battery import BatteryConfig
from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.commons.utils.utilities import format_float
from simses.technology.lithium_ion.cell.type import CellType


class BatteryManagementSystem:
    """ BatteryManagementSystem class """

    def __init__(self, cell_type: CellType, battery_config: BatteryConfig):
        self.__log: Logger = Logger(type(self).__name__)
        self.__cell: CellType = cell_type
        self.__min_soc = battery_config.min_soc
        self.__max_soc = battery_config.max_soc

    def update(self, time: float, battery_state: LithiumIonState, power_target: float) -> None:
        """Updating current of lithium_ion state in order to comply with cell type restrictions"""
        battery_state.max_charge_power = self.__get_max_charge_power(time, battery_state)
        battery_state.max_discharge_power = self.__get_max_discharge_power(time, battery_state)
        battery_state.current = self.__get_max_current(battery_state)
        self.__set_battery_fulfillment(power_target, battery_state)

    def __get_max_current(self, battery_state: LithiumIonState) -> float:
        if self.__temperature_in_range(battery_state):
            if not self.__current_in_range(battery_state):
                self.__log.warn("Battery current out of range: " + format_float(battery_state.current))
            voltage: float = battery_state.voltage
            max_charge_current: float = battery_state.max_charge_power / voltage
            max_discharge_current: float = -1.0 * battery_state.max_discharge_power / voltage
            current = max(min(battery_state.current, max_charge_current), max_discharge_current)
            if not max_discharge_current <= current <= max_charge_current:
                self.__log.warn('Current is limited due to SOC.')
            return current
        else:
            self.__log.warn("Battery temperature out of range: " + format_float(battery_state.temperature))
            return 0.0

    def __get_max_charge_power(self, time: float, battery_state: LithiumIonState):
        return min(abs(self.__cell.get_max_current(battery_state)),
                   abs(self.__soc_max_charge_current(time, battery_state))) * battery_state.voltage

    def __get_max_discharge_power(self, time: float, battery_state: LithiumIonState):
        return min(abs(self.__cell.get_min_current(battery_state)),
                   abs(self.__soc_max_discharge_current(time, battery_state))) * battery_state.voltage

    def __temperature_in_range(self, battery_state: LithiumIonState) -> bool:
        value = battery_state.temperature
        min_value = self.__cell.get_min_temp()
        max_value = self.__cell.get_max_temp()
        return self.__min_max_check(value, min_value, max_value)

    def __voltage_in_range(self, battery_state: LithiumIonState) -> bool:
        # Due to overvoltages this leads to an oscillation of input current and prohibits a full charge of the lithium_ion.
        # TODO implement e.g. linear restricition functions in order to ease current in min/max soc regions
        # return self.__cell.get_min_voltage() <= battery_state.voltage <= self.__cell.get_max_voltage()
        return True

    def __soc_in_range(self, battery_state: LithiumIonState) -> bool:
        value = battery_state.soc  # + RintModel.calculate_dsoc(time, battery_state, self.__cell)
        min_value = self.__min_soc
        max_value = self.__max_soc
        return self.__min_max_check(value, min_value, max_value)

    def __soc_max_charge_current(self, time: float, battery_state: LithiumIonState) -> float:
        denergy = (self.__max_soc - battery_state.soc) * battery_state.capacity
        current = denergy / battery_state.voltage_open_circuit / (time - battery_state.time) * 3600.0
        return max(0.0, current)

    def __soc_max_discharge_current(self, time: float, battery_state: LithiumIonState) -> float:
        denergy = (battery_state.soc - self.__min_soc) * battery_state.capacity
        current = denergy / battery_state.voltage_open_circuit / (time - battery_state.time) * 3600.0
        return min(0.0, -current)

    def __current_in_range(self, battery_state: LithiumIonState) -> bool:
        min_value = self.__cell.get_min_current(battery_state)
        max_value = self.__cell.get_max_current(battery_state)
        return self.__min_max_check(battery_state.current, min_value, max_value)

    def __set_battery_fulfillment(self, power_target: float, battery_state: LithiumIonState) -> None:
        power_is = battery_state.current * battery_state.voltage
        if abs(power_is - power_target) < 1e-6:
            battery_state.fulfillment = 1.0
        elif power_target == 0:
            self.__log.error('Power should be 0, but is ' + str(power_is) + ' W - Check BMS function')
            battery_state.fulfillment = 0.0
        else:
            battery_state.fulfillment = abs(power_is / power_target)
            if battery_state.fulfillment < 0 or battery_state.fulfillment > 1:
                self.__log.error('Fulfillment should be between 0 and 1 , but is ' +
                                 str(battery_state.fulfillment) + ' p.u. - Check BMS function')

    @staticmethod
    def __min_max_check(value: float, min_value: float, max_value: float) -> bool:
        return min_value <= value <= max_value

    def close(self) -> None:
        """Closing all resources in lithium_ion management system"""
        self.__log.close()
