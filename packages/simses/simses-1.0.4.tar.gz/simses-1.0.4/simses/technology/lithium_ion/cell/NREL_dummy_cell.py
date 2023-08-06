import math

import pandas as pd

from simses.commons.config.data.battery import BatteryDataConfig
from simses.commons.config.simulation.battery import BatteryConfig
from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.technology.lithium_ion.cell.type import CellType


class NRELDummyCell(CellType):
    """An GenericCell is a special cell type and inherited by CellType"""


    __CELL_VOLTAGE = 4  # V
    __CELL_CAPACITY = 2.5  # Ah

    pd.set_option('precision', 9)

    def __init__(self, voltage: float, capacity: float, soh: float, battery_config: BatteryConfig,
                 battery_data_config: BatteryDataConfig = None):
        super().__init__(voltage, capacity, soh, self.__CELL_VOLTAGE, self.__CELL_CAPACITY, battery_config)
        self.__log: Logger = Logger(type(self).__name__)
        self.__nominal_voltage = self.__CELL_VOLTAGE * self._SERIAL_SCALE  # V
        self.__max_voltage = (self.__CELL_VOLTAGE + 0.01) * self._SERIAL_SCALE  # V
        self.__min_voltage = (self.__CELL_VOLTAGE - 0.01) * self._SERIAL_SCALE  # V
        self.__capacity = self.__CELL_CAPACITY * self._PARALLEL_SCALE  # Ah
        self.__max_c_rate_charge = 2  # 1/h
        self.__max_c_rate_discharge = 2  # 1/h
        self.__max_current = self.__capacity * self.__max_c_rate_charge  # A
        self.__min_current = -self.__capacity * self.__max_c_rate_discharge  # A
        self.__coulomb_efficiency = 1 # Coulomb Efficiency is set to 1. Losses are calculated via internal resistance

        # Physical parameters for lithium_ion thermal model
        # Dummy parameters for dummy cell
        self.__mass = 0.05  # kg
        self.__diameter = 22  # mm
        self.__length = 70  # mm
        self.__volume = math.pi * self.__diameter**2 * self.__length/4 * 10**(-9)  # m3
        self.__surface_area = (2 * math.pi * self.__diameter/2 * self.__length + 2 * math.pi * (self.__diameter/2)**2) * 10**(-6)  # m2
        self.__specific_heat = 700  # J/kgK
        self.__convection_coefficient = 15  #


        self.__min_temperature = 273.15  # K
        self.__max_temperature = 333.15  # K

        # Self discharge is neglected in our simulations 0.015 / (30.5 * 24 * 3600) #1.5%-soc per month in second step
        self.__self_discharge_rate = 0
        self.__open_circuit_voltage = 4  # V
        self.__internal_resistance = 0.010  # Ohm


    def get_open_circuit_voltage(self, battery_state: LithiumIonState) -> float:
        return self.__open_circuit_voltage * self._SERIAL_SCALE

    def get_internal_resistance(self, battery_state: LithiumIonState) -> float:
        return float(self.__internal_resistance / self._PARALLEL_SCALE * self._SERIAL_SCALE)

    def get_self_discharge_rate(self) -> float:
        return self.__self_discharge_rate

    def get_coulomb_efficiency(self, battery_state: LithiumIonState) -> float:
        return self.__coulomb_efficiency if battery_state.is_charge else 1 / self.__coulomb_efficiency

    def get_nominal_voltage(self) -> float:
        return self.__nominal_voltage

    def get_min_current(self, battery_state: LithiumIonState) -> float:
        return self.__min_current

    def get_nominal_capacity(self) -> float:
        return self.__capacity

    def get_capacity(self, battery_state: LithiumIonState) -> float:
        return self.__capacity

    def get_max_current(self, battery_state: LithiumIonState) -> float:
        return self.__max_current

    def get_min_temp(self) -> float:
        return self.__min_temperature

    def get_max_temp(self) -> float:
        return self.__max_temperature

    def get_min_voltage(self) -> float:
        return self.__min_voltage

    def get_max_voltage(self) -> float:
        return self.__max_voltage

    def get_serial_scale(self) -> float:
        return self._SERIAL_SCALE

    def get_parallel_scale(self) -> float:
        return self._PARALLEL_SCALE

    def get_mass(self) -> float:
        return self.__mass * self._SERIAL_SCALE * self._PARALLEL_SCALE

    def get_surface_area(self):
        return self.__surface_area * self._SERIAL_SCALE * self._PARALLEL_SCALE

    def get_specific_heat(self):
        return self.__specific_heat

    def get_convection_coefficient(self):
        return self.__convection_coefficient

    def get_volume(self):
        return self.__volume * self._SERIAL_SCALE * self._PARALLEL_SCALE

    def close(self):
        self.__log.close()
